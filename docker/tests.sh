#!/bin/bash

alembic upgrade head

pytest -vv tests/