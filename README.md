# Simple Static Site Generator

A custom static site generator built in Python that converts Markdown files to HTML pages. This project was created as part of the Boot.dev curriculum.

## Features

- **Markdown to HTML conversion**: Supports all major markdown elements
  - Headings (H1-H6)
  - Paragraphs with inline formatting (bold, italic, code)
  - Lists (ordered and unordered)
  - Blockquotes
  - Code blocks
  - Links and images
- **Recursive page generation**: Processes entire directory structures
- **Configurable basepath**: Support for deployment to subdirectories
- **Template system**: Uses HTML templates with placeholder replacement
- **Static asset copying**: Automatically copies CSS, images, and other assets

## Usage

### Local Development
```bash
# Build and serve locally (uses "/" basepath)
bash main.sh
```

### Production Build
```bash
# Build for GitHub Pages (uses "/simple-static-gen/" basepath)
bash build.sh
```

### Custom Basepath
```bash
# Build with custom basepath
python3 src/main.py "/your-custom-path/"
```

## Project Structure

- `src/` - Python source code for the static site generator
- `content/` - Markdown content files
- `static/` - Static assets (CSS, images)
- `template.html` - HTML template with placeholders
- `docs/` - Generated site output (excluded from git)

## Testing

```bash
bash test.sh
```

## Deployment

This site is automatically deployed to GitHub Pages using GitHub Actions. The workflow builds the site and deploys it whenever changes are pushed to the main branch.

Visit the live site: https://victoralexander132.github.io/simple-static-gen/
