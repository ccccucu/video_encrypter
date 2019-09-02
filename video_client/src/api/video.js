import { ipcMain } from "electron";
import axios from "@/utils/request";
import httpAdapter from "@/utils/http";
import { SERVER_URL } from "./index";

export function videoDownload(videoId) {
  return axios({
    url: `${SERVER_URL}/videos/download/${videoId}`,
    method: "get",
    responseType: "stream",
    adapter: httpAdapter
  });
}

export function queryVideos(args) {
  return axios.post(`${SERVER_URL}/videos`, { _method: "GET", _args: args });
}

export function get_uuid() {
  var s = [];
  var hexDigits = "0123456789abcdef";
  for (var i = 0; i < 36; i++) {
    s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
  }
  s[14] = "4";
  s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);
  s[8] = s[13] = s[18] = s[23] = "-";

  var uuid = s.join("");
  return uuid;
}

export function postWaterMark(video_id, watermark) {
  var time = new Date();
  return axios.post(`${SERVER_URL}/watermark_logs`, {
    video_id: video_id,
    // "ip": user_info.ip,
    'watermark': watermark
  });
}

export function pingServer() {
  return axios.get(`${SERVER_URL}/ping`, {
    timeout: 1000
  });
}

export function searchWaterMark(q) {
  return axios.get(`${SERVER_URL}/watermark_logs/search?q=${q}`, {});
}
