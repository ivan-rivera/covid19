******************
COVID-19 Monitor
******************

NOTE: this project is currently under construction.

This application aims to explore the effects of the COVID-19 pandemic. The app is available `here <https://covid-monitor.herokuapp.com/>`_.


Ideas to implement:
    - Infection spread
        - filled world map based on number of infections and deaths (2 modes) (+ time lapse)
        - Time series of infections and deaths
        - Time series of gradients (indicate inflection point)
    - Financial impact
        - Foreign Exchange
        -
    - Travel
        - ???
    - In the media
        - Most liked tweets
        - Related Terms


Resources:
    - `JHU COVID API <https://covidapi.info/>`_ and `Pomber API <https://github.com/pomber/covid19>`_

..
    Setup Notes:
    - run `cp hooks/pre-commit .git/hooks/`
    - run `chmod +x .git/hooks/pre-commit`
    - After creating a new ENV switch to it via `poetry shell`
    - To install jupyter on this env use `python -m ipykernel install --name=myvenv`

..
    References:
    - favicon: https://favicon.io/emoji-favicons/biohazard/

..
    TODO:
    - Compile ideas (spread inflection + forecast, finance, travel + other ideas)
    - Find APIs
    - Find Dash tutorial + HTML/CSS/JS injection
    - Look to add the following into the project:
        - asyncio
        - pathlib X
        - typing X
        - logging X
        - caching X
        - data classes
    - Review resources
        - Dash tutorial: https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f