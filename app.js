const { App, ExpressReceiver } = require("@slack/bolt");
const extraRoutes = require("./express-wrapper");

const receiver = new ExpressReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  processBeforeResponse: true,
});
receiver.app.use(extraRoutes);

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
  receiver,
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡️ Slack bot is running securely with Socket Mode.");
})();
EOF < /dev/null