# Release Workflow Guide

This document explains how the automated build and release workflow works.

## Workflow Triggers

The workflow triggers on:

1. **Tag Push** - When you push a tag starting with `v` (e.g., `v1.0.0`)
   - Validates tag format (must match `v*.*.*` semantic versioning)
   - Builds executables for all platforms
   - Uploads artifacts to GitHub Actions (available for 30 days)
   - **Does NOT automatically attach to release** - you manually attach them

2. **Release Creation** - When you create a GitHub Release
   - Builds executables for all platforms
   - **Automatically attaches artifacts to the release**

3. **Manual Trigger** - Via GitHub Actions UI
   - Allows you to build without creating a tag or release

## Tag Format Validation

Tags must follow semantic versioning pattern:
- ✅ Valid: `v1.0.0`, `v2.3.4`, `v10.20.30`
- ❌ Invalid: `v1.0`, `1.0.0`, `v1.0.0-beta`, `v1`

## Workflow Process

### When You Push a Tag

```bash
git tag v1.0.0
git push origin v1.0.0
```

**What happens:**
1. Workflow triggers automatically
2. `validate-tag` job validates the tag format
3. If valid, builds run for Linux, Windows, and macOS
4. Artifacts are uploaded to GitHub Actions
5. **You manually download and attach to release**

**To attach artifacts:**
1. Go to **Actions** tab → Find the completed workflow run
2. Scroll to **Artifacts** section
3. Download: `linux-executables`, `windows-executables`, `macos-executables`
4. Go to **Releases** → Create/edit release for that tag
5. Drag and drop the downloaded files

### When You Create a Release

1. Go to **Releases** → "Draft a new release"
2. Select or create tag (e.g., `v1.0.0`)
3. Add release notes
4. Click "Publish release"

**What happens:**
1. Workflow triggers automatically
2. Builds executables for all platforms
3. **Automatically attaches all artifacts to the release**
4. Files are immediately available for download

## Artifact Retention

- Artifacts are kept for **30 days** in GitHub Actions
- After 30 days, they're automatically deleted
- Attach to releases quickly to preserve them permanently

## Best Practices

### Recommended Workflow

1. **Push tag first:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Wait for builds to complete** (5-10 minutes)
   - Check Actions tab for progress

3. **Create release:**
   - Go to Releases → Draft new release
   - Select the tag
   - Add release notes
   - **Download artifacts from Actions and attach them**
   - Publish release

### Alternative: Automatic Attachment

If you want automatic attachment:
1. Create the release first (don't push tag)
2. Workflow will build and attach automatically
3. Tag is created automatically when you publish the release

## Troubleshooting

### Tag Validation Failed

If you see "Invalid tag format":
- Check your tag follows `v*.*.*` pattern
- Example: `v1.0.0` ✅, not `v1.0` ❌

### Build Failed

- Check Actions tab for error messages
- Common issues:
  - Missing dependencies
  - PyInstaller errors
  - Platform-specific issues

### Artifacts Not Available

- Artifacts are only available after builds complete
- Check Actions tab → Workflow run → Artifacts section
- Artifacts expire after 30 days

## Summary

- **Tag push** → Builds artifacts → You manually attach
- **Release creation** → Builds artifacts → Automatically attaches
- **Tag format** → Must be `v*.*.*` (e.g., `v1.0.0`)

