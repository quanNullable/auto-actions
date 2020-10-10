const exec = require("child_process").execSync;
const fs = require("fs");
const download = require("download");
const rp = require("request-promise");

// 公共变量
const Secrets = {
  JD_COOKIE: process.env.JD_COOKIE, //cokie,多个用&隔开即可
  SyncUrl: process.env.SYNCURL, //签到地址,方便随时变动
  PUSH_KEY: process.env.PUSH_KEY, //server酱推送消息
};
async function downFile() {
  await download(Secrets.SyncUrl, "./", { filename: "temp.js" });
}

async function changeFile(content, cookie) {
  let newContent = content.replace(/var Key = ''/, `var Key = '${cookie}'`)
  await fs.writeFileSync("./execute.js", newContent, "utf8");
}

async function sendNotify(text, desp) {
  const options = {
    uri: `https://sc.ftqq.com/${Secrets.PUSH_KEY}.send`,
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

async function executeOneByOne() {
  let cookieJDs = [];
  cookieJDs = Secrets.JD_COOKIE.split("&");
  console.log(`当前共${cookieJDs.length}个账号需要签到`);
  const content = await fs.readFileSync("./temp.js", "utf8");
  for (var i = 0; i < cookieJDs.length; i++) {
    console.log(`正在执行第${i + 1}个账号签到任务`);
    await changeFile(content, cookieJDs[i]);
    console.log("替换变量完毕");
    try {
      await exec("node execute.js  >> result.txt", { stdio: "inherit" });
    } catch (e) {
      console.log("执行异常:" + e);
    }
    console.log(`第${i + 1}个账号签到任务执行完毕`);
  }
}

async function start() {
  console.log(`当前执行时间:${new Date().toString()}`);
  if (!Secrets.JD_COOKIE) {
    console.log("请填写 JD_COOKIE 后在继续");
    return;
  }
  if (!Secrets.SyncUrl) {
    console.log("请填写 SYNCURL 后在继续");
    return;
  }
  // 下载最新代码
  await downFile();
  console.log("下载代码完毕");
  await executeOneByOne();
  console.log("全部执行完毕");
  if (Secrets.PUSH_KEY) {
    const path = "./result.txt";
    let content = "";
    if (fs.existsSync(path)) {
      content = fs.readFileSync(path, "utf8");
    }
    await sendNotify("京东签到", content);
    console.log('发送结果完毕')
  }
}

start();