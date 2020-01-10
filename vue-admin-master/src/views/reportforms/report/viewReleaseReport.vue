<template>
    <section>
        <el-col :span="16" :offset="4">
            <el-form :model="viewForm" label-width="100px" label-position="20" ref="viewForm" >
                <el-form-item >
                    <h2 style="text-align: center;color: #48ace6">查看发布报告</h2>
                </el-form-item>
                <div>
                <el-form-item label="邮件主题" prop="subject">
                    <span>{{viewForm.subject}}</span>
                </el-form-item>
                <el-form-item label="收件人" prop="recipients">
                    <span>{{viewForm.recipients}}</span>
                </el-form-item>
                <el-form-item label="抄送人" prop="copier">
                    <span>{{viewForm.copier}}</span>
                </el-form-item>
                </div>
                <el-form-item label="一、版本号" >
                    <span>{{viewForm.version}}</span>
                </el-form-item>
                <el-form-item label="二、更新内容" >
                   <span>{{viewForm.updateContext}}</span>
                </el-form-item>
                <el-form-item label="三、需求列表" style="width: 100%;">
                    <div>
                        <el-table :data="viewForm.need">
                            <el-table-column prop="title" label="标题" width="400"></el-table-column>
                            <el-table-column prop="priority" label="优先级" width="120"></el-table-column>
                            <el-table-column prop="status" label="状态" width="120"></el-table-column>
                            <el-table-column prop="handler" label="处理人" width="150"></el-table-column>
                            <el-table-column prop="start_time" label="预计开始时间" width="150" sortable></el-table-column>
                            <el-table-column prop="end_time" label="预计结束时间" width="150" sortable></el-table-column>
                        </el-table>
                    </div>
                </el-form-item>
                <el-form-item label="四、测试报告" style="width: 100%;">
                    <span>{{viewForm.testReport}}</span>
                </el-form-item>
                <el-form-item label="五、注意事项" style="margin-top: 100px" >
                   <span>{{viewForm.attention}}</span>
                </el-form-item>
                <el-form-item label="报告分类" prop="type" hidden>
					<span>{{viewForm.type}}</span>
				</el-form-item>
            </el-form>
        </el-col>

    </section>
</template>

<script>
    import { getReport } from "../../../api/api.js";

    export default {
        data() {
            return {
                viewForm: {
                    id: 0,
                    subject: '',
                    recipients: '',
                    copier:'',
                    version: '',
                    updateContext: '',
                    need: '',
                    testReport: '',
                    attention: '',
                    type:2
                },
            }
        },
        methods: {
            setFormFieldValue(id){
                let para = {id:id}
                getReport(para).then((res) => {
                    let{code,result,msg} = res;
                    if (code=="200"){
                        this.viewForm=result;
                    }
                });
            },
        },
        mounted() {
           if(this.$route.query.id){
                this.setFormFieldValue(this.$route.query.id);
            }
            else{
                this.viewForm = this.$route.query.addForm;
            }
        }
    }

</script>

<style scoped>

</style>


