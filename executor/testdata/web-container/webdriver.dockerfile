FROM --platform=linux/amd64 ubuntu:22.04

WORKDIR /driver

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 unzip curl \
        openjdk-11-jre-headless \
        ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release xdg-utils && \
    curl  -L --fail-with-body -H 'Accept: application/octet-stream' -o selenium-server.jar https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.24.0/selenium-server-4.24.0.jar && \
    curl  -L --fail-with-body -H 'Accept: application/octet-stream' -o chrome-driver.zip https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/linux64/chromedriver-linux64.zip && \
    curl  -L --fail-with-body -H 'Accept: application/octet-stream' -o chrome.zip https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/linux64/chrome-linux64.zip && \
    unzip chrome-driver.zip && \
    unzip chrome.zip && \
    rm chrome-driver.zip chrome.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/driver/chromedriver-linux64/:/driver/chrome-linux64/:${PATH}"

RUN useradd -m appuser && chown -R appuser:appuser /driver

USER appuser
EXPOSE 4444

COPY entry.sh /driver/entry.sh
COPY server.py /driver/server.py

CMD ["/driver/entry.sh"]
