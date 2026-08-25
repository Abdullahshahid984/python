ARG PARENT_VERSION=2.5.2-node22.13.1
ARG PARENT_RUNTIME_VERSION=${PARENT_VERSION}
ARG PARENT_DEV_VERSION=${PARENT_VERSION}
ARG NPM_VERSION=11.6.4
ARG PORT=3000
ARG PORT_DEBUG=9229

FROM defradigital/node-development:${PARENT_DEV_VERSION} AS development

ENV TZ="Europe/London"

ARG PARENT_DEV_VERSION
ARG NPM_VERSION
LABEL uk.gov.defra.ffc.parent-image=defradigital/node-development:${PARENT_DEV_VERSION}

ARG PORT
ARG PORT_DEBUG
ENV PORT=${PORT}
EXPOSE ${PORT} ${PORT_DEBUG}

# Force Alpine upgrade in development layer
USER root
RUN apk update && apk upgrade --no-cache
USER node

# Setup stable global package tools
RUN npm install --global npm@${NPM_VERSION} && npm cache clean --force

WORKDIR /home/node

COPY --chown=node:node --chmod=755 package*.json ./

# Run full project setup tracking custom tree overrides block
RUN npm install --ignore-scripts --legacy-peer-deps
COPY --chown=node:node . .
RUN npm run build

CMD [ "npm", "run", "dev" ]

FROM development AS production_build

ENV NODE_ENV=production
RUN npm run build

FROM defradigital/node:${PARENT_RUNTIME_VERSION} AS production

ENV TZ="Europe/London"

# Force Alpine runtime layer upgrades to ensure 0 OS vulnerabilities
USER root
ARG NPM_VERSION
RUN apk update && apk upgrade --no-cache \
    && apk add --no-cache curl \
    && npm install --global npm@${NPM_VERSION} \
    && npm cache clean --force

USER node
WORKDIR /home/node

ARG PARENT_RUNTIME_VERSION
LABEL uk.gov.defra.ffc.parent-image=defradigital/node:${PARENT_RUNTIME_VERSION}

COPY --from=production_build /home/node/package*.json ./
COPY --from=production_build /home/node/.server ./.server/
COPY --from=production_build /home/node/.public/ ./.public/

# Mirror isolated production dependencies seamlessly 
RUN npm i --omit=dev --ignore-scripts --legacy-peer-deps

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD [ "node", "." ]
