<template>
    <section>
        <el-col :span="16" :offset="4">
            <el-form :model="viewForm" label-width="150px" label-position="20" ref="viewForm" >
                <el-form-item >
                    <h2 style="text-align: center;color: #48ace6">查看测试报告</h2>
                </el-form-item>
                <div>
                <el-form-item label="邮件主题" prop="subject">
                    <span>{{viewForm.subject}}</span>
                </el-form-item>
                <el-form-item label="收件人" prop="recipient">
                    <span>{{viewForm.recipient}}</span>
                </el-form-item>
                    <el-form-item label="抄送人" prop="copier">
                    <span>{{viewForm.copier}}</span>
                </el-form-item>
                </div>
                <el-form-item label="一、测试结论" >
                    <span>{{viewForm.conclusion}}</span>
                </el-form-item>
                <el-form-item label="二、测试目的" >
                   <span>{{viewForm.purposes}}</span>
                </el-form-item>
                <el-form-item label="三、测试环境" >
                    <span>{{viewForm.environment}}</span>
                </el-form-item>
                <el-form-item label="四、版本需求列表">
                    <el-table :data="viewForm.need">
                        <el-table-column prop="title" label="标题" width="300"></el-table-column>
                        <el-table-column prop="priority" label="优先级" width="80"></el-table-column>
                        <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="80"></el-table-column>
                        <el-table-column prop="status" label="状态" width="80"></el-table-column>
                        <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                        <el-table-column prop="start_time" label="预计开始时间" width="140" sortable></el-table-column>
                        <el-table-column prop="end_time" label="预计结束时间" width="140" sortable></el-table-column>
                    </el-table>
                </el-form-item>
                <el-form-item label="五、版本缺陷列表">
                   <el-table :data="viewForm.bug">
                       <el-table-column prop="title" label="标题" width="300"></el-table-column>
                       <el-table-column prop="severity" label="严重程度" width="80"></el-table-column>
                       <el-table-column prop="priority" label="优先级" width="80"></el-table-column>
                       <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
                       <el-table-column prop="status" label="状态" width="80"></el-table-column>
                       <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                       <el-table-column prop="creater" label="创建人" width="100" sortable></el-table-column>
                       <el-table-column prop="createTime" label="创建时间" width="140" sortable></el-table-column>
                   </el-table>
                </el-form-item>
                <el-form-item label="六、测试用例" style="margin-top: 100px" >
                    <div><span>{{viewForm.useCase}}</span></div>
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
                    id:0,
                    subject: '',
                    recipient: '',
                    copier:'',
                    conclusion: '',
                    purposes: '',
                    need:[],
                    bug:[],
                    useCase: '',
                    type:1
                },
                iterationJson:{"1":"当前迭代","2":"后续迭代","3":"已完成迭代"},
            }
        },
        methods: {
             //将迭代格式化，数字转成文字
			formatIteration(row){
				if(row.iteration){
					return this.iterationJson[row.iteration];
				}
			},
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
                this.setFormFieldValue(this.$route.query.id)
            }
            else if(this.$route.query.addForm){
                this.viewForm = this.$route.query.addForm;
            }
            else{
                this.viewForm = this.$route.query.editForm;

                this.viewForm.recipient = this.viewForm.names;
                this.viewForm.copier = this.viewForm.copier_names;




            }
        }
    }

</script>

<style scoped>

</style>


