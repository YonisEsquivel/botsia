virtualenv env
env\Scripts\activate.bat
pip install dash pandas plotly requests
pip install dash-bootstrap-components
pip install bta-lib
pip install mysql-connector-python
pip freeze

pip freeze > requirements.txt

pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
set "FLASK_DEBUG=development"
