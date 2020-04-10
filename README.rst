******************
COVID-19 Monitor
******************


A tiny Heroku app that visualizes the spread of COVID-19 throughout the world. The app is available `here <https://covid-monitor.herokuapp.com/>`_.

Here is a screenshot of the app.

.. image:: resources/screenshot.png


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