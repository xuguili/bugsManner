<template>
    <section>
        <el-col :span="16" :offset="4" >
            <el-form class="addPage" label-width="100px" label-position="20" :model="addForm" :rules="addFormRules" ref="addForm">
                <el-form-item >
                    <h2 style="text-align: center;color: #48ace6">创建测试报告</h2>
                </el-form-item>
                <el-form-item>
                    <h3 style="text-align: left;color: #000000">基本信息</h3>
                </el-form-item>
                <el-form-item label="邮件主题" prop="subject" style="width: 500px;">
                    <el-input v-model="addForm.subject" clearable></el-input>
                </el-form-item>
                <el-form-item label="收件人" prop="recipient" style="width: 100%;">
					<el-select v-model="addForm.recipient" multiple clearable placeholder="请选择">
						<el-option v-for="item in recipients" :label="item.loginName" :key="item.email" :value="item.email"></el-option>
					</el-select>
				</el-form-item>
                <el-form-item label="抄送人" prop="copier" style="width: 100%;">
                    <el-select v-model="addForm.copier" multiple placeholder="请选择" style="width: 40%">
                        <el-option v-for="item in copiers" :label="item.loginName" :key="item.email" :value="item.email"></el-option>
                    </el-select>
                </el-form-item>
                 <el-form-item>
                    <h3 style="text-align: left;color: #000000">邮件内容</h3>
                </el-form-item>
                <el-form-item label="测试结论" >
                    <el-input v-model="addForm.conclusion" clearable></el-input>
                </el-form-item>
                <el-form-item label="测试目的" >
                    <el-input v-model="addForm.purposes" clearable></el-input>
                </el-form-item>
                <el-form-item label="测试环境" >
                    <el-input v-model="addForm.environment"></el-input>
                </el-form-item>
                <el-form-item label="版本需求列表">
                    <el-button v-model="addForm.currentneed" type="primary" size="medium" icon="el-icon-plus" v-on:click="handleAdd">选择需求</el-button>
                    <div>
                        <el-table :data="currentneed">
                            <el-table-column prop="title" label="标题" width="400"></el-table-column>
                            <el-table-column prop="priority" label="优先级" width="100"></el-table-column>
                            <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
                            <el-table-column prop="status" label="状态" width="100"></el-table-column>
                            <el-table-column prop="handler" label="处理人" width="130"></el-table-column>
                            <el-table-column prop="start_time" label="预计开始时间" width="140" sortable></el-table-column>
                            <el-table-column prop="end_time" label="预计结束时间" width="140" sortable></el-table-column>
                        </el-table>
                    </div>
                </el-form-item>
                <el-form-item label="版本缺陷列表">
                    <el-button v-model="addForm.currentbug" type="primary" size="medium" icon="el-icon-plus" v-on:click="handleAddBug">选择缺陷</el-button>
                    <div>
                        <el-table :data="currentbug">
                            <el-table-column prop="title" label="标题" width="400"></el-table-column>
                            <el-table-column prop="severity" label="严重程度" width="100"></el-table-column>
                            <el-table-column prop="priority" label="优先级" width="100"></el-table-column>
                            <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
                            <el-table-column prop="status"  label="状态" width="100"></el-table-column>
                            <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                            <el-table-column prop="creater" label="创建人" width="100" sortable></el-table-column>
                            <el-table-column prop="createTime" label="创建时间" width="140" sortable></el-table-column>
                        </el-table>
                    </div>
                </el-form-item>
                <el-form-item label="测试用例">
                    <el-upload class="upload-demo" ref="upload" action="http://localhost:5000/reportForms/report/addReport"
                               name="file" :data="addForm" :on-success="submitSuccesss" :auto-upload="false">
                        <el-button slot="trigger" size="medium" icon="el-icon-folder" type="primary">选取文件</el-button>

                    </el-upload>
                </el-form-item>
                <el-form-item label="报告分类" prop="type" hidden>
					<el-select v-model="addForm.type" filterable clearable placeholder="请选择">
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

        <!--版本需求列表-->
		<el-dialog title="选择版本需求" v-model="listNeedVisible" :visible.sync="listNeedVisible" width="60%">
			<!--工具条-->
			<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
				<el-form :inline="true" :model="filters">
					<el-form-item>
					<el-input v-model="filters.title"  size="medium" placeholder="标题" clearable></el-input>
					</el-form-item>
					<el-form-item>
					<el-input v-model="filters.handler"  size="medium" placeholder="处理人" clearable></el-input>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" size="medium" icon="el-icon-search" v-on:click="searchNeed">搜索</el-button>
					</el-form-item>
				</el-form>
			</el-col>
			<el-table :data="need" highlight-current-row v-loading="listLoading" @selection-change="selectionChange" style="width: 100%;">
				<el-table-column type="selection" width="60"></el-table-column>
				<el-table-column type="index" width="60"></el-table-column>
				<el-table-column prop="title" label="标题" width="400"></el-table-column>
				<el-table-column prop="priority" label="优先级"  width="100" ></el-table-column>
                <el-table-column prop="iteration" label="迭代" :formatter="formatIteration"  width="100"></el-table-column>
				<el-table-column prop="status" label="状态" width="100"></el-table-column>
				<el-table-column prop="handler" label="处理人" width="140"></el-table-column>
				<el-table-column prop="start_time" label="预计开始时间" width="140" sortable></el-table-column>
				<el-table-column prop="end_time" label="预计结束时间" width="140" sortable></el-table-column>
			</el-table>
			<!--工具条-->
			<div slot="footer" class="dialog-footer">
				<el-button size="small" type="primary" style="float: left" @click="addSubmit()" :disabled="this.selection.length==0">添加</el-button>
				<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="filters.currentPage"
								   :page-sizes="[10,20,30]" :page-size="filters.size" layout="total,sizes,prev,pager,next,jumper" :total="total">
				</el-pagination>
			</div>
		</el-dialog>

         <!--版本缺陷列表-->
		<el-dialog title="选择版本缺陷" v-model="listBugVisible" :visible.sync="listBugVisible" width="60%">
			<!--工具条-->
			<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
				<el-form :inline="true" :model="filters">
					<el-form-item>
					<el-input v-model="filters.title"  size="medium" placeholder="标题" clearable></el-input>
					</el-form-item>
					<el-form-item>
					<el-input v-model="filters.handler"  size="medium" placeholder="处理人" clearable></el-input>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" size="medium" icon="el-icon-search" v-on:click="searchBug">搜索</el-button>
					</el-form-item>
				</el-form>
			</el-col>
			<el-table :data="bug" highlight-current-row v-loading="listLoading" @selection-change="selectionChange" style="width: 100%;">
				<el-table-column type="selection" width="60"></el-table-column>
				<el-table-column type="index" width="60"></el-table-column>
                <el-table-column prop="title" label="标题" width="400"></el-table-column>
                <el-table-column prop="severity" label="严重程度" width="100"></el-table-column>
                <el-table-column prop="priority" label="优先级" width="100"></el-table-column>
                <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
                <el-table-column prop="status"  label="状态" width="100"></el-table-column>
                <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                <el-table-column prop="creater" label="创建人" width="100" sortable></el-table-column>
                <el-table-column prop="createTime" label="创建时间" width="140" sortable></el-table-column>
			</el-table>
			<!--工具条-->
			<div slot="footer" class="dialog-footer">
				<el-button size="small" type="primary" style="float: left" @click="addSubmit1()" :disabled="this.selection.length==0">添加</el-button>
				<el-pagination @size-change="handleSizeChange1" @current-change="handleCurrentChange1" :current-page="filters.currentPage1"
								   :page-sizes="[10,20,30]" :page-size="filters.size1" layout="total,sizes,prev,pager,next,jumper" :total="total1">
				</el-pagination>
			</div>
		</el-dialog>
    </section>
</template>

<script>
    import { getUserName,listNeed,listBug } from "../../../api/api.js";

    export default {
        data() {
            return {
                filters:{
                    title:'',
                    handler:'',
                    currentPage:1,
					size:10,
                    currentPage1:1,
					size1:10,
                },
                bug: [],
                copiers:'',
                recipients:'',
                selection:[],
				need:[],
                currentneed:[],
                currentbug:[],
                listNeedVisible:false,
                listBugVisible:false,
                listLoading:false,
                total:0,
                total1:0,
                iterationJson:{"1":"当前迭代","2":"后续迭代","3":"已完成迭代"},
                uploadData:{
                    name:'',
                    type:'welcome',

                },
                addForm: {
                    subject: '',
                    recipient: '',
                    copier:'',
                    conclusion: '',
                    purposes: '',
                    need:'',
                    bug:'',
                    useCase: '',
                    type:1,
                    isSend:''
                },
                addFormRules: {
                    subject: [{required: true, message: '请输入邮件主题', trigger: 'blur'}],
                    recipient: [{required: true, message: '请选择收件人', trigger: 'blur'}]
                },
            }
        },
        methods: {

            handleCancle() {
                this.$router.push('/reportforms/report/1');
            },
            //预览邮件
            handleView(){
                this.$router.push({path:'/viewTestReport',query: { addForm: this.addForm }});

            },
            handleAdd(){
				this.listneed();
			},
            handleAddBug(){
				this.listbug();
			},
            searchNeed(){
				this.filters.page=1;
				this.listneed();
			},
            searchBug(){
				this.filters.page=1;
				this.listbug();
			},
            listneed(){
				this.listNeedVisible = true;
				let needParams = {
					title:this.filters.title,
					handler:this.filters.handler,
					page:this.filters.currentPage,
					size:this.filters.size,
				}

				this.listLoading=true;
				listNeed(needParams).then((res) => {
					this.total = res.total;
					this.need = res.needList;
					this.listLoading = false;
				});
			},
            listbug(){
				this.listBugVisible = true;
				let bugParams = {
					title:this.filters.title,
					handler:this.filters.handler,
					page:this.filters.currentPage1,
					size:this.filters.size1,
				}

				this.listLoading=true;
				listBug(bugParams).then((res) => {
					this.total1 = res.total;
					this.bug = res.bugList;
					this.listLoading = false;
				});
			},
            getUsername(){
                let userParams = {};
                getUserName(userParams).then((res) => {
                    this.recipients = res.user;
                    this.copiers = res.user;
                });
            },
            selectionChange:function(selection){
				this.selection = selection;
			},
            handleSizeChange(val){
				this.filters.size = val;//当前显示条数
				this.listneed();
			},
            handleSizeChange1(val){
				this.filters.size1= val;//当前显示条数
				this.listbug();
			},
             handleCurrentChange(val){
				this.filters.currentPage = val;//当前页
				this.listneed();
			},
            handleCurrentChange1(val){
				this.filters.currentPage1 = val;//当前页
				this.listbug();
			},
             //将迭代格式化，数字转成文字
			formatIteration(row){
				if(row.iteration){
					return this.iterationJson[row.iteration];
				}
			},

            // 选择需求并显示出来
			addSubmit: function () {
				this.currentneed = this.selection;
				this.listNeedVisible=false;
			},
             // 选择缺陷并显示出来
			addSubmit1: function () {
				this.currentbug = this.selection;
				this.listBugVisible=false;
			},

            // handleFilePreview(file){
            //     console.log(file);
            // },
            // handleFileRemove(){
            //     console.log(file);
            // },
            //发送邮件即新增报告
            sendMail: function (isSend) {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认添加吗？', '提示', {}).then(() => {
                            this.addForm.isSend = isSend;

                            this.addForm.recipient = this.addForm.recipient.join(",");
                            this.addForm.copier = this.addForm.copier.join(",");

                            let ids = new Array();
                            for (let i in this.currentneed){
                                ids.push(this.currentneed[i].id);
                            }
                            this.addForm.need = ids.toString();

                            let bug_ids = new Array();
                            for (let i in this.currentbug){
                                bug_ids.push(this.currentbug[i].id);
                            }
                            this.addForm.bug = bug_ids.toString();

                            this.$refs.upload.submit();

                        });
                    }
                });
            },
            submitSuccesss:function(response, file, fileList){
                if('success'==response){
                    this.$message({
                        message: '添加成功',
                        type: 'success'
                    });
                    this.$refs['addForm'].resetFields();
                    this.$router.push('/reportforms/report/1');
                }
            }
        },
        mounted() {
            this.getUsername();
            }
    }

</script>

<style scoped>
    .addPage{
        min-width: 950px;
        width: 1200px;
    }

</style>
