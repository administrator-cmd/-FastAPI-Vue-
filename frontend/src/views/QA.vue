<template>
  <div class="qa-container">
    <el-card class="qa-card">
      <template #header>
        <div class="card-header">
          <span>🤖 智能问答</span>
        </div>
      </template>

      <!-- 提问区域 -->
      <div class="question-section">
        <el-input
          v-model="question"
          type="textarea"
          :rows="4"
          placeholder="请输入你的问题..."
          maxlength="2000"
          show-word-limit
          :disabled="loading"
        />
        <el-button
          type="primary"
          @click="handleAsk"
          :loading="loading"
          :disabled="!question.trim()"
          style="margin-top: 10px; width: 100%"
        >
          提问
        </el-button>
      </div>

      <!-- 当前回答 -->
      <div v-if="currentAnswer" class="answer-section">
        <el-divider>AI 回答</el-divider>
        <div class="answer-content">
          <div v-html="renderMarkdown(currentAnswer.answer)"></div>
          <div class="answer-meta">
            <el-tag size="small" type="info">
              {{ formatTime(currentAnswer.created_at) }}
            </el-tag>
          </div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div v-if="qaHistory.length > 0" class="history-section">
        <el-divider>历史记录</el-divider>
        <el-timeline>
          <el-timeline-item
            v-for="record in qaHistory"
            :key="record.id"
            :timestamp="formatTime(record.created_at)"
            placement="top"
          >
            <el-card>
              <div class="history-item">
                <div class="question-text">
                  <strong>问：</strong>{{ record.question }}
                </div>
                <div class="answer-text">
                  <div v-html="renderMarkdown(record.answer)"></div>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>

      <!-- 空状态 -->
      <el-empty
        v-if="!currentAnswer && qaHistory.length === 0"
        description="暂无问答记录，开始提问吧！"
      />
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import dayjs from 'dayjs'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt()

export default {
  name: 'QA',
  data() {
    return {
      question: ''
    }
  },
  computed: {
    ...mapState('qa', ['qaHistory', 'currentAnswer', 'loading'])
  },
  created() {
    this.fetchQAHistory()
  },
  methods: {
    ...mapActions('qa', ['askQuestion', 'fetchQAHistory']),
    
    renderMarkdown(text) {
      return md.render(text)
    },
    
    async handleAsk() {
      if (!this.question.trim()) return
      
      try {
        await this.askQuestion({
          question: this.question.trim(),
          context: null
        })
        this.question = ''
        this.$message.success('提问成功')
      } catch (error) {
        console.error('提问失败:', error)
      }
    },
    
    formatTime(time) {
      return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
    }
  }
}
</script>

<style scoped>
.qa-container {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.qa-card {
  min-height: 600px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.question-section {
  margin-bottom: 20px;
}

.answer-section {
  margin-top: 20px;
}

.answer-content {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.8;
}

.answer-meta {
  margin-top: 10px;
  text-align: right;
}

.history-section {
  margin-top: 30px;
}

.history-item {
  line-height: 1.8;
}

.question-text {
  margin-bottom: 10px;
  color: #409eff;
}

.answer-text {
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .qa-container {
    padding: 0 10px;
  }
}
</style>
