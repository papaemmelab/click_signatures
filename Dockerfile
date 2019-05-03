FROM papaemmelab/docker-signatures:1.0.0

# install click_signatures
COPY . /code
RUN pip3 install /code && rm -rf /code

# add entry point
ENTRYPOINT ["click_signatures"]
