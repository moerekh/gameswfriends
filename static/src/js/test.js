const { Issuer } = require('openid-client');
Issuer.discover('https://steamcommunity.com/openid') // => Promise
.then(function (steamIssuer) {
    console.log('Discovered issuer %s %O', steamIssuer.issuer, steamIssuer.metadata);
});