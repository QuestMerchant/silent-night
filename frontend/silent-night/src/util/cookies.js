export function setCookie(cname, cvalue, exdays) {
    const d = new Date()
    d.setTime(d.getTime() + (exdays*24*60*60*1000))
    const expires = "expires="+ d.toUTCString()
    document.cookie = cname + "=" + cvalue + ";" + expires + "; path=/"
  }
  
  export function fetchCookie(cname) {
    const name = cname + "="
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.startsWith(name)) {
        return cookie.substring(name.length)
      }
    }
    return null
  }