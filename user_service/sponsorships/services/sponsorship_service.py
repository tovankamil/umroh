# sponsorships/services/sponsorship_service.py
from django.db import connection
from collections import defaultdict
from sponsorships.models import Sponsorship
from users.models import CustomUser
from django.db.models import Count, Q

class SponsorshipService:    
    BONUS_RULES = {
        1: {'required_level': 'SPP', 'amount': 100000},
        2: {'required_level': 'SM', 'amount': 100000},
        3: {'required_level': 'SD', 'amount': 100000},
    }
    
    @classmethod
    def get_upline_with_bonus(cls, user_id, max_level=4):
        """
        Mendapatkan upline dengan perhitungan bonus
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH RECURSIVE user_upline AS (
                    SELECT
                        s.id,
                        s.user_id,
                        s.sponsor_id,
                        0 AS level,
                        u.username,
                        u.level_status
                    FROM
                        sponsorships_sponsorship AS s
                    JOIN
                        users_customuser AS u ON s.user_id = u.id
                    WHERE
                        s.user_id = %s
                    
                    UNION ALL
                    
                    SELECT
                        t.id,
                        t.user_id,
                        t.sponsor_id,
                        h.level + 1,
                        u.username,
                        u.level_status
                    FROM
                        sponsorships_sponsorship AS t
                    JOIN
                        user_upline AS h ON h.sponsor_id = t.user_id
                    JOIN
                        users_customuser AS u ON t.user_id = u.id
                    WHERE
                        h.sponsor_id IS NOT NULL 
                        AND h.level < %s
                )
                SELECT * FROM user_upline
            """, [user_id, max_level])
            
            rows = cursor.fetchall()
            return cls.calculate_level_status_detailed(rows,user_id)
    
    @classmethod
    def calculate_level_status_detailed(cls, rows=None,user_id=None):
        """
       Update status level
        """       
        if rows is None:
            rows = []
            
        results = []
        level_changed = []
        for i, row in enumerate(rows):
            try:
                if user_id is not None and len(row) > 1 and str(user_id) == str(row[1]):
                 print(f"{i}. Skipping row karena user_id {user_id} == row[1] {row[1]}")
                 continue  # Lanjut ke row berikutnya
                
                if len(row) <= 2:
                    raise IndexError("Format row tidak valid")
                    
                sponsor = CustomUser.objects.get(id=row[2])
                
                # Hitung berdasarkan berbagai level status
                agent_stats = Sponsorship.objects.filter(sponsor=sponsor).aggregate(
                    total_agents=Count('user'),
                    agent_count=Count('user', filter=Q(user__level_status=CustomUser.LevelStatus.AGENT)),
                    supervisor_count=Count('user', filter=Q(user__level_status=CustomUser.LevelStatus.SUPERVISOR)),
                    manager_count=Count('user', filter=Q(user__level_status=CustomUser.LevelStatus.MANAGER)),
                    director_count=Count('user', filter=Q(user__level_status=CustomUser.LevelStatus.DIRECTOR))
                )
                
                if agent_stats['agent_count'] >=20: # Minimal 20 agen untuk naik level ke supervisor
                    new_level = cls.determine_level_based_on_agents(agent_stats['agent_count'])
                    if sponsor.level_status != new_level:
                        sponsor.level_status = new_level
                        sponsor.save()
                        currentlevel = {
                            index:i,
                            level:1
                        }   
                        level_changed.append(currentlevel)
                if agent_stats['supervisor_count'] >=15: # Minimal 20 agen untuk naik level ke seniormanager
                    new_level = cls.determine_level_based_on_agents(agent_stats['supervisor_count'])
                    if sponsor.level_status != new_level:
                        sponsor.level_status = new_level
                        sponsor.save()
                        currentlevel = {
                            index:i,
                            level:2
                        }   
                        level_changed.append(currentlevel)
                if agent_stats['manager_count'] >=10: # Minimal 20 agen untuk naik level ke director
                    new_level = cls.determine_level_based_on_agents(agent_stats['manager_count'])
                    if sponsor.level_status != new_level:
                        sponsor.level_status = new_level
                        sponsor.save()
                        currentlevel = {
                            index:i,
                            level:3
                        }   
                        level_changed.append(currentlevel)
                
                result = {
                    'index': i,
                    'sponsor_id': sponsor.id,
                    'sponsor_username': sponsor.username,
                    'total_members': agent_stats['total_agents'],
                    'agent_count': agent_stats['agent_count'],
                    'supervisor_count': agent_stats['supervisor_count'],
                    'manager_count': agent_stats['manager_count'],
                    'director_count': agent_stats['director_count'],
                    'currentlevel': level_changed
                }
                
                results.append(result)
                print(f"{i}. {sponsor.username}: {agent_stats['agent_count']} Agents {level_changed}")
                
            except CustomUser.DoesNotExist:
                print(f"{i}. Error: Sponsor dengan ID {row[2]} tidak ditemukan")
            except (IndexError, ValueError) as e:
                print(f"{i}. Error: {e}")
        
        return results

            
    @classmethod
    def determine_level_based_on_agents(cls, agent_count):
        """
        Menentukan level status berdasarkan jumlah agen
        (Anda bisa menyesuaikan logika bisnisnya)
        """
        if agent_count >= 10:
            return CustomUser.LevelStatus.DIRECTOR
        elif agent_count >= 15:
            return CustomUser.LevelStatus.MANAGER
        elif agent_count >= 20:
            return CustomUser.LevelStatus.SUPERVISOR
        else:
            return CustomUser.LevelStatus.AGENT
    
    @classmethod
    def _calculate_bonus(cls, rows):
        """
        Menghitung bonus berdasarkan rules (business logic terpisah)
        """
        results = []
        for row in rows:
            level = row[3]  # level dari query
            level_status = row[5]  # level_status dari query
            
            bonus = 0
            if level in cls.BONUS_RULES:
                rule = cls.BONUS_RULES[level]
                if level_status == rule['required_level']:
                    bonus = rule['amount']
            
            results.append({
                'id': row[0],
                'user_id': row[1],
                'sponsor_id': row[2],
                'level': level,
                'username': row[4],
                'level_status': level_status,
                'bonus': bonus
            })
        
        return results

    # Tambahkan method ini jika ingin caching
    @classmethod
    def get_upline_with_bonus_cached(cls, user_id, max_level=3):
        """
        Versi cached dari get_upline_with_bonus
        """
        # Implementasi caching bisa ditambahkan di sini
        return cls.get_upline_with_bonus(user_id, max_level)