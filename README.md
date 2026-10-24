<!--
  Every image is a <picture>: GitHub loads assets/dark/<name>.svg when the visitor
  uses a dark theme, and the light assets/<name>.svg otherwise (also the fallback).
  assets/dark/ is generated: run `python3 scripts/build-themes.py` after editing a light SVG.
-->

<!-- Hero Banner & About Me / Currently Bento -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/Hero-Banner.svg" />
    <img src="./assets/Hero-Banner.svg" width="100%" align="top" alt="Shrey Singh aka MrPanda009" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/bento-about-currently.svg" />
    <img src="./assets/bento-about-currently.svg" width="100%" align="top" alt="About Me and Current Focus" />
  </picture>
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

<!-- Tech Stack, Live GitHub Stats & Socials (upcoming)
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/dark/bento-bottom.svg" />
    <img src="./assets/bento-bottom.svg" width="100%" alt="Tech Stack and GitHub Stats" />
  </picture>
</p>
-->
