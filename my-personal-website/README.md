# Personal Website

A modern personal website built with VitePress, inspired by the RSSHub documentation site.

## Features

- Responsive design for all devices
- Dark/light mode support
- Content organized in a structured, documentation-style format
- Fast and efficient static site generation

## Tech Stack

- **VitePress**: Vue-powered static site generator
- **Vue.js**: Progressive JavaScript framework
- **TypeScript**: Typed JavaScript
- **CSS**: Custom styling with CSS variables for theming

## Getting Started

### Prerequisites

- Node.js (>= 16.0.0)
- npm or pnpm

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-website.git
   cd personal-website
   ```

2. Install dependencies:
   ```bash
   npm install
   # or with pnpm
   pnpm install
   ```

3. Start the development server:
   ```bash
   npm run docs:dev
   # or with pnpm
   pnpm docs:dev
   ```

4. Open your browser and visit `http://localhost:5173`

### Building for Production

To build the site for production:

```bash
npm run docs:build
# or with pnpm
pnpm docs:build
```

The built site will be in the `.vitepress/dist` directory, which can be deployed to any static hosting service.

## Customization

### Site Configuration

Modify the VitePress configuration in `docs/.vitepress/config.ts` to customize the site's appearance and behavior.

### Content

Content is written in Markdown files located in the `docs` directory. The structure follows VitePress conventions:

- `index.md` - Home page
- `about/index.md` - About page
- `projects/index.md` - Projects page
- etc.

## License

MIT 