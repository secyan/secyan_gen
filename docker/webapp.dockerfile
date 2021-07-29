FROM node:14 as build

WORKDIR /app
COPY ./webapp/ ./
RUN yarn install
ENV PUBLIC_URL=/
ENV REACT_APP_URL=http://0.0.0.0:5000
ENV GENERATE_SOURCEMAP false
RUN yarn build

# production environment
FROM nginx:stable
COPY --from=build /app/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]