ARG PARENT_VERSION=3.0.0-node22.14.0
ARG PARENT_RUNTIME_VERSION=${PARENT_VERSION}
ARG PARENT_DEV_VERSION=${PARENT_VERSION}
ARG NPM_VERSION=11.15.0
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

# FIX 1: Upgrade NPM engine first before copying package files to prevent legacy engine warnings
RUN npm install --global npm@${NPM_VERSION} && npm cache clean --force

WORKDIR /home/node

# FIX 2: Copy both package.json and your modified package-lock.json with your overrides
COPY --chown=node:node --chmod=755 package*.json ./

RUN npm install --ignore-scripts
COPY --chown=node:node . .
RUN npm run build

CMD [ "npm", "run", "dev" ]

FROM development AS production_build

ENV NODE_ENV=production
RUN npm run build

FROM defradigital/node:${PARENT_RUNTIME_VERSION} AS production

ENV TZ="Europe/London"

USER root
ARG NPM_VERSION

# FIX 3: Run full Alpine package cleanup to patch OS-level Trivy violations
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

# FIX 4: Run clean production install utilizing your lockfile overrides
RUN npm ci --omit=dev --ignore-scripts

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD [ "node", "." ]
