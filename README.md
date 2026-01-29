# Content Tree Dashboard

Analytics dashboard for Worksection Marketing Content System.

**Live:** https://marakinpoetry.github.io/content-tree-dashboard/

## Features

- 538 content files tracked
- Google Drive clickable links
- Search across all content
- Progress charts by stage, language, type
- Smart gap analysis & recommendations

## Update Dashboard

```bash
# From CONTENT TREE root:
python3 generate_gdrive_mapping.py  # Update Google Drive IDs
python3 Dashboard/update_dashboard.py  # Regenerate data.json

# Deploy:
cp Dashboard/data.json Dashboard/deploy/
cd Dashboard/deploy
git add data.json
git commit -m "Update dashboard data"
git push
```
