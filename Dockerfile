COPY --chown=node:node package.json ./
RUN npm install --global npm@${NPM_VERSION} \
    && npm cache clean --force
RUN npm install --ignore-scripts
COPY --chown=node:node . .
RUN npm install tar@7.5.19 minimatch@10.2.3 glob@11.1.0 brace-expansion@2.1.2 ip-address@10.3.1 picomatch@4.0.4 --save
RUN npm run build
