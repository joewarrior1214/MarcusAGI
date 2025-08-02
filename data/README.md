# Data Directory

This directory contains all database files and data storage for Marcus AGI.

## Structure

- **`active/`** - Currently active database files
- **`backups/`** - Database backups and historical versions

## Database Files

### Active Databases
- `marcus_memory.db` - Main memory system database
- `marcus_consciousness.db` - Consciousness state and integration data
- `marcus_embodied.db` - Embodied learning and physical interaction data
- `marcus_spatial_learning.db` - Spatial awareness and navigation data

### Backup Strategy
- Daily automated backups are stored in `backups/`
- Naming convention: `[database_name]_YYYYMMDD_HHMMSS.bak`
