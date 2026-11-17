---
layout: page
title: projects
permalink: /projects/
description: Inference systems I have designed and optimized.
nav: true
nav_order: 3
---

<div class="project-grid">
{% assign sorted_projects = site.projects | sort: "importance" %}
{% for project in sorted_projects %}
  {% include projects.liquid %}
{% endfor %}
</div>
