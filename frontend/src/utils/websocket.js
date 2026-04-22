class WebSocketClient {
  constructor() {
    this.ws = null
    this.reconnectTimer = null
    this.heartbeatTimer = null
    this.listeners = {}
    this.isConnected = false
  }

  /**
   * 连接 WebSocket
   * @param {string} token - JWT token
   */
  connect(token) {
    if (this.ws && this.isConnected) {
      console.warn('WebSocket 已连接')
      return
    }

    // 直接连接后端 8000 端口
    const wsUrl = `ws://127.0.0.1:8000/api/v1/ws/chat?token=${token}`

    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket 连接成功')
      this.isConnected = true
      this.startHeartbeat()
      this.trigger('connected', {})
    }

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('收到消息:', data)
      this.trigger(data.type, data)
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket 错误:', error)
      this.trigger('error', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket 连接关闭')
      this.isConnected = false
      this.stopHeartbeat()
      this.trigger('disconnected', {})
      this.reconnect(token)
    }
  }

  /**
   * 发送消息
   * @param {string} type - 消息类型
   * @param {object} data - 消息数据
   */
  send(type, data = {}) {
    if (!this.ws || !this.isConnected) {
      console.error('WebSocket 未连接')
      return
    }

    this.ws.send(JSON.stringify({ type, ...data }))
  }

  /**
   * 发送聊天消息
   * @param {string} content - 消息内容
   * @param {number|null} receiverId - 接收者ID（null为群聊）
   */
  sendMessage(content, receiverId = null) {
    this.send('chat_message', {
      content,
      receiver_id: receiverId
    })
  }

  /**
   * 监听事件
   * @param {string} event - 事件名称
   * @param {function} callback - 回调函数
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = []
    }
    this.listeners[event].push(callback)
  }

  /**
   * 移除监听
   * @param {string} event - 事件名称
   * @param {function} callback - 回调函数
   */
  off(event, callback) {
    if (!this.listeners[event]) return
    
    if (callback) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback)
    } else {
      delete this.listeners[event]
    }
  }

  /**
   * 触发事件
   * @param {string} event - 事件名称
   * @param {*} data - 事件数据
   */
  trigger(event, data) {
    if (!this.listeners[event]) return
    
    this.listeners[event].forEach(callback => {
      callback(data)
    })
  }

  /**
   * 开始心跳
   */
  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      this.send('ping')
    }, 30000) // 每30秒发送一次心跳
  }

  /**
   * 停止心跳
   */
  stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }

  /**
   * 重连
   * @param {string} token - JWT token
   */
  reconnect(token) {
    if (this.reconnectTimer) return
    
    console.log('尝试重连...')
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      this.connect(token)
    }, 3000) // 3秒后重连
  }

  /**
   * 断开连接
   */
  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    
    this.stopHeartbeat()
    
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    
    this.isConnected = false
  }
}

// 导出单例
export default new WebSocketClient()
