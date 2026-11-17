---
layout: page
title: projects
permalink: /projects/
description: Inference systems I have designed and optimized.
nav: true
nav_order: 3
---

<!-- pages/projects.md -->
<div class="projects">
{% assign sorted_projects = site.projects | sort: "importance" %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
</div>
