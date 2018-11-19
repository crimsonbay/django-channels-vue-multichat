const serverIP = 'localhost'
const serverPort = '8000'
const serverAddr = serverIP + ':' + serverPort
console.log(serverAddr)

export function fetchAddUser (login, name, password) {
  return fetch('http://' + serverAddr + '/api/add-user?username=' + login +
    '&first_name=' + name +
    '&password=' + password, {
    method: 'POST',
    mode: 'cors'
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function fetchGetAllChats () {
  return fetch('http://' + serverAddr + '/api/get-chats?all=true', {
    method: 'GET',
    mode: 'cors'
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function fetchLeaveChat (chatName) {
  let token = sessionStorage.getItem('token')
  return fetch('http://' + serverAddr + '/api/leave-chat?chatname=' + chatName, {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Authorization': 'Token ' + token
    } })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function fetchGetUserChats () {
  let token = sessionStorage.getItem('token')
  let headerAuth = {}
  if (token) {
    headerAuth = {
      'Authorization': 'Token ' + token
    }
  }
  return fetch('http://' + serverAddr + '/api/get-chats', {
    method: 'GET',
    mode: 'cors',
    headers: headerAuth
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function fetchGetMessages (chatName) {
  let token = sessionStorage.getItem('token')
  let headerAuth = {}
  if (token) {
    headerAuth = {
      'Authorization': 'Token ' + token
    }
  }
  return fetch('http://' + serverAddr + '/api/get-messages?chatname=' + chatName, {
    method: 'GET',
    mode: 'cors',
    headers: headerAuth
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function newSocket (chatName) {
  let token = sessionStorage.getItem('token')
  var mySocket = new WebSocket('ws://' + serverAddr + '/ws/chat/' + chatName + '?token=' + token)
  return mySocket
}

export function fetchCheckToken (token) {
  return fetch('http://' + serverAddr + '/api/check-token', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + token
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

export function fetchAPITokenAuth (name, password) {
  return fetch('http://' + serverAddr + '/api/api-token-auth/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'username': name,
      'password': password })
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}
