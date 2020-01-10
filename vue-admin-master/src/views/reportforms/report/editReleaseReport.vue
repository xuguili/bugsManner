<template>
    <section>
        <el-col :span="16" :offset="4">
            <el-form :model="editForm" label-width="100px" label-position="20" :rules="editFormRules" ref="editForm" >
                <el-form-item >
                    <h2 style="text-align: center;color: #48ace6">编辑发布报告</h2>
                </el-form-item>
                <el-form-item label="邮件主题" prop="subject">
                    <el-input v-model="editForm.subject" clearable></el-input>
                </el-form-item>
               <el-form-item label="收件人" prop="recipient">
					<el-select v-model="editForm.recipient" filterable clearable placeholder="请选择">
						<el-option v-for="item in recipients" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
                <el-form-item label="抄送人" prop="copier">
                    <el-select v-model="editForm.copier" filterable placeholder="请选择" style="width: 40%">
                        <el-option v-for="item in copier" :key="item.label" :label="item.label" :value="item.label"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="版本号" >
                    <el-input v-model="editForm.version" clearable></el-input>
                </el-form-item>
                <el-form-item label="更新内容" >
                    <el-input v-model="editForm.updateContext" clearable></el-input>
                </el-form-item>
                <el-form-item label="需求列表" style="width: 50%;float: left">
                    <el-select v-model="editForm.need" filterable  placeholder="请选择" style="width: 100%;">
                        <el-option key="1" label="需求一" value=1></el-option>
                        <el-option key="2" label="需求二" value=2></el-option>
                        <el-option key="3" label="需求三" value=3></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="测试报告" style="width: 50%;float: left">
                    <el-input v-model="editForm.testReport"></el-input>
                </el-form-item>
                <el-form-item label="注意事项" style="margin-top: 146px" >
                    <el-input v-model="editForm.attention"></el-input>
                </el-form-item>
                <el-form-item label="报告分类" prop="type" hidden>
					<el-select v-model="editForm.type" filterable clearable placeholder="请选择">
						<el-option key="1" label="测试报告" value=1></el-option>
						<el-option key="2" label="发布报告" value=2></el-option>
					</el-select>
				</el-form-item>
                <el-form-item >
                    <el-button type="primary" @click.native="sendMail('Y')" >发送邮件</el-button>
                    <el-button type="primary" @click.native="handleView" >邮件预览</el-button>
                    <el-button type="primary" @click.native="sendMail('N')" >保存草稿</el-button>
                    <el-button type="primary" @click.native="handleCancle" >取消</el-button>
                </el-form-item>
            </el-form>
        </el-col>

    </section>
</template>

<script>
    import { editReport,getReport,getUserName } from "../../../api/api.js";

    export default {
        data() {
            return {
                recipients:'',
                copier:[{label:'1774454505@qq.com'}],
                editForm: {
                    id: 0,
                    subject: '',
                    recipient: '',
                    copier:'',
                    version: '',
                    updateContext: '',
                    need: '',
                    testReport: '',
                    attention: '',
                    type:2
                },
                editFormRules: {
                    subject: [{required: true, message: '请输入邮件主题', trigger: 'blur'}],
                    recipient: [{required: true, message: '请选择收件人', trigger: 'blur'}]
                },
            }
        },
        methods: {
            handleCancle() {
                this.$router.push('/reportforms/report/2');
            },
            getUsername(){
                let userParams = {};
                getUserName(userParams).then((res) => {
                    this.recipients = res.user;
                });
            },
            //编辑
            sendMail: function (isSend) {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认添加吗？', '提示', {}).then(() => {
                            this.editForm.isSend = isSend;
                            let para = Object.assign({}, this.editForm);
                            editReport(para).then((res) => {
                                this.$message({
                                    message: '编辑成功',
                                    type: 'success'
                                });
                                this.$refs['editForm'].resetFields();
                                this.$router.push('/reportforms/report/2');
                            });
                        });
                    }

                });
            },
            setFormFieldValue(id){
                let para = {id:id}
                getReport(para).then((res) => {
                    let{code,result,msg} = res;
                    if (code=="200"){
                        this.editForm=result;
                    }
                });
            },
        },
        mounted() {
            if (this.$route.query.id) {
                this.setFormFieldValue(this.$route.query.id);
            }
            this.getUsername();
        }
    }

</script>

<style scoped>

</style>
