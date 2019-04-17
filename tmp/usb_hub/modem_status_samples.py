# -*- coding: UTF-8 -*-

# Sample statuses of different modems.
# Useful for developing automated tests
# with locking/unlocking SIM cards via PIN and PUK code.

output_unlocked1 = """    
  Status   |           lock: 'none'
           | unlock retries: 'unknown'
           |          state: 'disconnecting'
           |    power state: 'on'
           |    access tech: 'gprs, 1xrtt, evdo0'
           | signal quality: '100' (recent)
"""

output_unlocked2 = """
  Status   |           lock: 'none'
           | unlock retries: 'sim-pin (3), sim-pin2 (3), sim-puk (10), sim-puk2 (10)'
           |          state: 'registered'
           |    power state: 'on'
           |    access tech: 'umts'
           | signal quality: '20' (recent)

"""

output_pin = """    
  Status   |           lock: 'sim-pin'
           | unlock retries: 'sim-pin (3), sim-puk (10)'
           |          state: 'locked'
           |    power state: 'on'
           |    access tech: 'unknown'
           | signal quality: '0' (cached)
"""

output_puk = """
  Status   |           lock: 'sim-puk'
           | unlock retries: 'sim-puk (10)'
           |          state: 'locked'
           |    power state: 'on'
           |    access tech: 'unknown'
           | signal quality: '0' (cached)
"""
