<!--
  Every image is a <picture>: GitHub loads assets/dark/<name>.svg when the visitor
  uses a dark theme, and the light assets/<name>.svg otherwise (also the fallback).
  assets/dark/ and assets/composed/ are generated: run `python3 scripts/build-themes.py` after editing a light SVG.
  The GITHUB_STATS numbers and grid are refreshed daily by .github/workflows/update-stats.yml.
-->

<!-- Hero Banner, About Me / Currently Bento and Tech Stack / GitHub Stats Bento, stacked into ONE image by
     scripts/compose.py (separate stacked images leave a faint seam line on 1x screens). Edit the parts in assets/. -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/composed/dark/profile.svg" />
    <img src="./assets/composed/profile.svg" width="100%" alt="Shrey Singh (MrPanda009): building useful things at the intersection of code, AI and real-world impact. About me, what I'm currently working on, tech stack and live GitHub stats." />
  </picture>
</p>

<!-- LET'S_CONNECT: one linked pixel button per link (links inside a single README image can't be clicked).
     Portfolio has no link yet: its button is dashed and muted. -->
<p align="center">
  <a href="https://github.com/MrPanda009"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/dark/btn-github.svg" /><img src="./assets/btn-github.svg" height="40" alt="GitHub" /></picture></a>
  <a href="https://www.linkedin.com/in/shrey-singh-70898237b/"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/dark/btn-linkedin.svg" /><img src="./assets/btn-linkedin.svg" height="40" alt="LinkedIn" /></picture></a>
  <a href="https://x.com/MrPanda009w"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/dark/btn-x.svg" /><img src="./assets/btn-x.svg" height="40" alt="X (Twitter)" /></picture></a>
  <a href="mailto:shrey33005@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/dark/btn-email.svg" /><img src="./assets/btn-email.svg" height="40" alt="Email" /></picture></a>
  <picture><source media="(prefers-color-scheme: dark)" srcset="./assets/dark/btn-portfolio.svg" /><img src="./assets/btn-portfolio.svg" height="40" alt="Portfolio (coming soon)" /></picture>
</p>

<!-- Featured Projects Header (upcoming)
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/header-projects.svg" />
    <img src="./assets/header-projects.svg" width="100%" alt="Featured Projects" />
  </picture>
</p>
-->

<!-- Clickable Project Cards Side-by-Side (upcoming)
<p align="center">
  <a href="https://github.com/MrPanda009/SETU-DRR">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/card-setu-drr.svg" />
      <img src="./assets/card-setu-drr.svg" width="32%" alt="SETU-DRR" />
    </picture>
  </a>
  <a href="https://github.com/MrPanda009/Nyay-AI-Liard">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/card-nyay-ai.svg" />
      <img src="./assets/card-nyay-ai.svg" width="32%" alt="Nyay-AI-Liard" />
    </picture>
  </a>
  <a href="https://github.com/MrPanda009/AWS-Auditor">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/card-aws-auditor.svg" />
      <img src="./assets/card-aws-auditor.svg" width="32%" alt="AWS Auditor" />
    </picture>
  </a>
</p>
-->
