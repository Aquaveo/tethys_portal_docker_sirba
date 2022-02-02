{% set CONDA_HOME = salt['environ.get']('CONDA_HOME') %}
{% set TETHYS_PERSIST = salt['environ.get']('TETHYS_PERSIST') %}
{% set STATIC_ROOT = salt['environ.get']('STATIC_ROOT') %}

Move_Custom_Theme_Files_to_Static_Root:
  cmd.run:
    - name: mv /tmp/custom_theme {{ STATIC_ROOT }}
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/custom_theme_setup_complete" ];"

Apply_Custom_Theme:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys site
        --title "My Custom Portal"
        --tab-title "My Custom Portal"
        --library-title "Tools"
        --primary-color "#01200F"
        --secondary-color "#358600"
        --background-color "#ffffff"
        --logo "/custom_theme/images/leaf-logo.png"
        --favicon "/custom_theme/images/favicon.ico"
        --copyright "Copyright © 2022 My Organization"
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/custom_theme_setup_complete" ];"

Flag_Custom_Theme_Setup_Complete:
  cmd.run:
    - name: touch {{ TETHYS_PERSIST }}/custom_theme_setup_complete
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/custom_theme_setup_complete" ];"
