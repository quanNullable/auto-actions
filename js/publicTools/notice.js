import rp from 'request-promise'

// 公共变量
const PUSH_KEY = process.env.PUSH_KEY //server酱推送消息

async function sendNotify(text, desp) {
  const options = {
    uri: `https://sc.ftqq.com/${PUSH_KEY}.send`,
    form: { text, desp },
    json: true,
    method: 'POST'
  }
  await rp.post(options).then(res => {
    console.log('发送通知成功', res)
  }).catch((err) => {
    console.log('发送通知失败', err)
  })
}

export { sendNotify }