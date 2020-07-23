/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  
  return str.length > 4
}

/* 判空验证 */
export function isEmpty(str) {
  const reg = /^\s*$/g;
  return reg.test(str);
}
