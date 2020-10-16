const rp = require('request-promise')

// 公共变量
const PUSH_KEY = process.env.PUSH_KEY //server酱推送消息

async function sendNotify(text, desp) {
  if (!PUSH_KEY) {
    console.log('发送通知失败', '请先配置PUSH_KEY')
    return false
  }
  const options = {
    uri: `https://sc.ftqq.com/${PUSH_KEY}.send`,
    form: { text, desp },
    json: true,
    method: 'POST'
  }
  await rp.post(options).then(res => {
    console.log('发送通知成功', res)
    return true
  }).catch((err) => {
    console.log('发送通知失败', err)
    return false
  })
}

module.exports = {
  sendNotify
};