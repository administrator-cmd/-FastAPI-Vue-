<template>
  <div class="chat-layout">
    <!-- 左侧用户列表 -->
    <div class="user-list">
      <div class="user-list-header">
        <h3>在线用户</h3>
        <div class="connection-status" :class="{ connected: isConnected }">
          {{ isConnected ? '●' : '○' }}
        </div>
      </div>
      
      <div class="user-list-body">
        <div 
          v-for="user in otherUsers" 
          :key="user.id"
          class="user-item"
          :class="{ active: selectedUserId === user.id }"
          @click="selectUser(user)"
        >
          <div class="user-avatar">{{ user.username[0].toUpperCase() }}</div>
          <div class="user-info">
            <div class="user-name">{{ user.username }}</div>
            <div class="user-last-message">{{ getLastMessage(user.id) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧聊天区 -->
    <div class="chat-area">
      <template v-if="selectedUser">
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="user-avatar small">{{ selectedUser.username[0].toUpperCase() }}</div>
            <span class="chat-title">{{ selectedUser.username }}</span>
          </div>
        </div>

        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="msg in currentMessages" 
            :key="msg.id" 
            class="message"
            :class="{ 'my-message': msg.sender_id === currentUserId }"
          >
            <div class="message-header">
              <span class="sender-name">{{ msg.sender_name || '用户' }}</span>
              <span class="message-time">{{ formatTime(msg.created_at) }}</span>
            </div>
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>

        <div class="chat-input">
          <input 
            v-model="newMessage" 
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
            :disabled="!isConnected"
          />
          <button @click="sendMessage" :disabled="!isConnected || !newMessage.trim()">
            发送
          </button>
        </div>
      </template>
      
      <div v-else class="no-chat-selected">
        <div class="empty-icon">💬</div>
        <p>选择一个用户开始聊天</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import wsClient from '@/utils/websocket'
import request from '@/utils/request'

export default {
  name: 'Chat',
  data() {
    return {
      users: [],
      messages: [],
      selectedUserId: null,
      newMessage: '',
      isConnected: false
    }
  },
  computed: {
    ...mapState('auth', ['currentUser', 'token']),
    currentUserId() {
      return this.currentUser?.id
    },
    otherUsers() {
      return this.users.filter(u => u.id !== this.currentUserId)
    },
    selectedUser() {
      return this.otherUsers.find(u => u.id === this.selectedUserId) || null
    },
    currentMessages() {
      if (!this.selectedUserId) return []
      
      // 筛选当前对话的消息（私聊）
      return this.messages.filter(msg => 
        (Number(msg.sender_id) === Number(this.currentUserId) && Number(msg.receiver_id) === Number(this.selectedUserId)) ||
        (Number(msg.sender_id) === Number(this.selectedUserId) && Number(msg.receiver_id) === Number(this.currentUserId))
      )
    }
  },
  mounted() {
    this.initWebSocket()
    this.loadUsers()
  },
  beforeUnmount() {
    wsClient.disconnect()
  },
  watch: {
    selectedUserId() {
      this.scrollToBottom()
    },
    currentMessages() {
      this.scrollToBottom()
    }
  },
  methods: {
    initWebSocket() {
      if (!this.token) {
        this.$router.push('/login')
        return
      }

      wsClient.on('connected', () => {
        this.isConnected = true
        this.loadChatHistory()
      })

      wsClient.on('disconnected', () => {
        this.isConnected = false
      })

      wsClient.on('new_message', (data) => {
        console.log('收到 new_message 事件:', data)
        console.log('当前 messages 数组:', this.messages)
        this.messages.push(data)
        console.log('push 后的 messages 数组:', this.messages)
        console.log('currentUserId:', this.currentUserId, 'selectedUserId:', this.selectedUserId)
        console.log('currentMessages:', this.currentMessages)
      })

      wsClient.connect(this.token)
    },

    async loadUsers() {
      try {
        const response = await request.get('/users')
        this.users = response
      } catch (error) {
        console.error('加载用户列表失败:', error)
      }
    },

    async loadChatHistory() {
      try {
        const response = await request.get('/ws/chat/history')
        this.messages = response.reverse()
      } catch (error) {
        console.error('加载聊天记录失败:', error)
      }
    },

    selectUser(user) {
      this.selectedUserId = user.id
    },

    getLastMessage(userId) {
      const userMessages = this.messages.filter(msg => 
        (Number(msg.sender_id) === Number(this.currentUserId) && Number(msg.receiver_id) === Number(userId)) ||
        (Number(msg.sender_id) === Number(userId) && Number(msg.receiver_id) === Number(this.currentUserId))
      )
      if (userMessages.length === 0) return '暂无消息'
      const lastMsg = userMessages[userMessages.length - 1]
      return lastMsg.content.substring(0, 20) + (lastMsg.content.length > 20 ? '...' : '')
    },

    sendMessage() {
      if (!this.newMessage.trim() || !this.selectedUserId) return
      
      wsClient.sendMessage(this.newMessage, this.selectedUserId)
      this.newMessage = ''
    },

    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: calc(100vh - 60px);
  background: #f5f5f5;
}

/* 左侧用户列表 */
.user-list {
  width: 300px;
  background: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.user-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.user-list-header h3 {
  margin: 0;
  font-size: 18px;
}

.connection-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ff4444;
}

.connection-status.connected {
  background: #00C851;
}

.user-list-body {
  flex: 1;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.user-item:hover {
  background: #f5f5f5;
}

.user-item.active {
  background: #e3f2fd;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  margin-right: 12px;
}

.user-avatar.small {
  width: 32px;
  height: 32px;
  font-size: 14px;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.user-last-message {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 右侧聊天区 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e0e0e0;
  background: white;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #fafafa;
}

.message {
  margin-bottom: 15px;
  max-width: 70%;
}

.my-message {
  margin-left: auto;
  text-align: right;
}

.message-header {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.my-message .message-header {
  justify-content: flex-end;
}

.message-content {
  padding: 10px 15px;
  border-radius: 10px;
  background: white;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.my-message .message-content {
  background: #007bff;
  color: white;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.chat-input input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.no-chat-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.no-chat-selected p {
  font-size: 16px;
}
</style>
