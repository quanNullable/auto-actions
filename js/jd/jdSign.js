const exec = require("child_process").execSync;
const fs = require("fs");
const download = require("download");
const rp = require("request-promise");
const { sendNotify } = require('../publicTools/notice.js')

// 公共变量
const JD_COOKIE = process.env.JD_COOKIE //cokie,多个用&隔开即可
const SyncUrl = 'https://raw.githubusercontent.com/NobyDa/Script/master/JD-DailyBonus/JD_DailyBonus.js'

async function downFile() {
  await download(SyncUrl, "./", { filename: "temp.js" });
}

async function changeFile(content, cookie) {
  let newContent = content.replace(/var Key = ''/, `var Key = '${cookie}'`)
  await fs.writeFileSync("./execute.js", newContent, "utf8");
}

async function executeOneByOne() {
  let cookieJDs = [];
  cookieJDs = JD_COOKIE.split("&");
  console.log(`当前共${cookieJDs.length}个账号需要签到`);
  const content = await fs.readFileSync("./temp.js", "utf8");
  for (var i = 0; i < cookieJDs.length; i++) {
    console.log(`正在执行第${i + 1}个账号签到任务`);
    await changeFile(content, cookieJDs[i]);
    console.log("替换变量完毕");
    try {
      console.log('22222222',exec("ls"))
      await exec("node js/jd/execute.js  >> result.txt", { stdio: "inherit" });
    } catch (e) {
      console.log("执行异常:" + e);
    }
    console.log(`第${i + 1}个账号签到任务执行完毕`);
  }
}

async function start() {
  console.log(`当前执行时间:${new Date().toString()}`);
  // if (!JD_COOKIE) {
  //   console.log("请填写 JD_COOKIE 后在继续");
  //   return;
  // }
  // 下载最新代码
  await downFile();
  console.log("下载代码完毕");
  await executeOneByOne();
  console.log("签到执行完毕");
  // await sendResult()
  // console.log("全部执行完毕");
}

async function sendResult(){
  const path = "./result.txt";
  let content = "";
  if (fs.existsSync(path)) {
    content = fs.readFileSync(path, "utf8");
  }
  if (!(await sendNotify("京东签到", content))) {
    console.log('京东签到', content)
  }
}

function formatSeconds(value) {
  var theTime = parseInt(value);// 需要转换的时间秒 
  var theTime1 = 0;// 分 
  var theTime2 = 0;// 小时 
  var theTime3 = 0;// 天
  if (theTime > 60) {
    theTime1 = parseInt(theTime / 60);
    theTime = parseInt(theTime % 60);
    if (theTime1 > 60) {
      theTime2 = parseInt(theTime1 / 60);
      theTime1 = parseInt(theTime1 % 60);
      if (theTime2 > 24) {
        //大于24小时
        theTime3 = parseInt(theTime2 / 24);
        theTime2 = parseInt(theTime2 % 24);
      }
    }
  }
  var result = '';
  if (theTime > 0) {
    result = "" + parseInt(theTime) + "秒";
  }
  if (theTime1 > 0) {
    result = "" + parseInt(theTime1) + "分" + result;
  }
  if (theTime2 > 0) {
    result = "" + parseInt(theTime2) + "小时" + result;
  }
  if (theTime3 > 0) {
    result = "" + parseInt(theTime3) + "天" + result;
  }
  return result;
}

start()

// var time = Math.random() * 1000 * 60 * 60 * 3
// console.log(formatSeconds(time / 1000) + "后开始执行签到")
// setTimeout(() => {
//   start()
// }, time);