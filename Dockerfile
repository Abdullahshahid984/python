
RUN npm install --global npm@${NPM_VERSION} && npm cache clean --force
COPY --chown=node:node --chmod=755 package*.json ./
RUN npm install --ignore-scripts
COPY --chown=node:node . .
RUN npm run build
