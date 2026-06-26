source "https://rubygems.org"

# Matches the GitHub Pages native build environment (Jekyll 3.x + whitelisted plugins).
# Lets `bundle exec jekyll serve` locally mirror what Pages produces.
gem "github-pages", group: :jekyll_plugins

# Plugins enabled in _config.yml (also bundled with github-pages, listed for clarity)
group :jekyll_plugins do
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
end

# Windows / JRuby timezone data (harmless elsewhere)
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]
