# services/sponsorship_service.py
from django.db import connection
from collections import defaultdict

class SponsorshipService:
    
    BONUS_RULES = {
        1: {'required_level': 'SPP', 'amount': 100000},
        2: {'required_level': 'SM', 'amount': 100000},
        3: {'required_level': 'SD', 'amount': 100000},
    }
    
    @classmethod
    def get_upline_with_bonus(cls, user_id, max_level=3):
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
            return cls._calculate_bonus(rows)
    
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