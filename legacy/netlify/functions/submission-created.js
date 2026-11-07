// Netlify automatically fires this function on every form submission.
// Formats the lead into a Slack Block Kit card and posts to the webhook.
// Requires env var: SLACK_WEBHOOK_URL

exports.handler = async (event) => {
  try {
    const body = JSON.parse(event.body || '{}');
    const data = (body.payload && body.payload.data) || {};

    const webhook = process.env.SLACK_WEBHOOK_URL;
    if (!webhook) {
      console.error('SLACK_WEBHOOK_URL env var is not set');
      return { statusCode: 500, body: 'no webhook configured' };
    }

    const name = (data.name || 'Unknown').toString().trim();
    const phone = (data.phone || 'Not provided').toString().trim();
    const email = (data.email || '(no email)').toString().trim();
    const projectType = (data['project-type'] || 'Not specified').toString().trim();
    const message = (data.message || '(no message)').toString().trim();

    const slackPayload = {
      // Fallback text for notifications
      text: `🏡 New lead: ${name} ,  ${phone}`,
      blocks: [
        {
          type: 'header',
          text: { type: 'plain_text', text: `🏡 New Palermo Homes Lead`, emoji: true },
        },
        {
          type: 'section',
          fields: [
            { type: 'mrkdwn', text: `*Name*\n${name}` },
            { type: 'mrkdwn', text: `*Phone*\n<tel:${phone}|${phone}>` },
            { type: 'mrkdwn', text: `*Project type*\n${projectType}` },
            { type: 'mrkdwn', text: `*Email*\n${email}` },
          ],
        },
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `*Message*\n${message}` },
        },
        {
          type: 'context',
          elements: [
            {
              type: 'mrkdwn',
              text: `Submitted via palermohomes.com contact form · ${new Date().toLocaleString('en-CA', { timeZone: 'America/Vancouver' })} PT`,
            },
          ],
        },
      ],
    };

    const res = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(slackPayload),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error('Slack webhook failed:', res.status, errText);
      return { statusCode: 502, body: `slack error: ${res.status}` };
    }

    return { statusCode: 200, body: 'ok' };
  } catch (err) {
    console.error('function error:', err);
    return { statusCode: 500, body: 'error' };
  }
};
