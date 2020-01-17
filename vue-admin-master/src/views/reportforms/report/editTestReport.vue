<template>
    <section>
        <el-col :span="16" :offset="4">
            <el-form :model="editForm" label-width="100px" label-position="20" :rules="editFormRules" ref="editForm" >
                <el-form-item >
                    <h2 style="text-align: center;color: #48ace6">编辑测试报告</h2>
                </el-form-item>
                <el-form-item label="邮件主题" prop="subject">
                    <el-input v-model="editForm.subject" clearable></el-input>
                </el-form-item>
                <el-form-item label="收件人" prop="recipient">
					<el-select v-model="editForm.recipient" multiple clearable placeholder="请选择" >
						<el-option v-for="item in recipients" :label="item['loginName']" :key="item['email']" :value="item['email']"></el-option>
					</el-select>
				</el-form-item>
                 <el-form-item label="抄送人" prop="copier">
                    <el-select v-model="editForm.copier" multiple placeholder="请选择" style="width: 40%">
                        <el-option v-for="item in copiers" :label="item['loginName']" :key="item['email']" :value="item['email']"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="测试结论" >
                    <el-input v-model="editForm.conclusion" clearable></el-input>
                </el-form-item>
                <el-form-item label="测试目的" >
                    <el-input v-model="editForm.purposes" clearable></el-input>
                </el-form-item>
                <el-form-item label="测试环境" >
                    <el-input v-model="editForm.environment"></el-input>
                </el-form-item>
                <el-form-item label="版本需求列表">
                    <el-button type="primary" size="medium" icon="el-icon-plus" v-on:click="handleAdd">选择需求</el-button>
                    <el-table :data="currentneed"><!-- 展示  -->
                        <el-table-column prop="title" label="标题" width="300"></el-table-column>
                        <el-table-column prop="priority" label="优先级" width="80"></el-table-column>
                        <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="80"></el-table-column>
                        <el-table-column prop="status" label="状态" width="80"></el-table-column>
                        <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                        <el-table-column prop="start_time" label="预计开始时间" width="140" sortable></el-table-column>
                        <el-table-column prop="end_time" label="预计结束时间" width="140" sortable></el-table-column>
                        <el-table-column width="80">
				            <template slot-scope="scope">
					            <a title="移除" class="el-icon-close" @click="handleRemove(scope.$index)"></a>
				            </template>
			            </el-table-column>
                    </el-table>
                </el-form-item>
                <el-form-item label="版本缺陷列表">
                    <el-button  type="primary" size="medium" icon="el-icon-plus" v-on:click="handleAddBug">选择缺陷</el-button>
                    <el-table :data="currentbug">
                       <el-table-column prop="title" label="标题" width="300"></el-table-column>
                       <el-table-column prop="severity" label="严重程度" width="80"></el-table-column>
                       <el-table-column prop="priority" label="优先级" width="80"></el-table-column>
                       <el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
                       <el-table-column prop="status" label="状态" width="80"></el-table-column>
                       <el-table-column prop="handler" label="处理人" width="140"></el-table-column>
                       <el-table-column prop="creater" label="创建人" width="100" sortable></el-table-column>
                       <el-table-column prop="createTime" label="创建时间" width="140" sortable></el-table-column>
                       <el-table-column width="80">
				            <template slot-scope="scope">
					            <a title="移除" class="el-icon-close" @click="handleRemove1(scope.$index)"></a>
				            </template>
			            </el-table-column>
                   </el-table>
                </el-form-item>
                <el-form-item label="测试用例">
                     <el-upload  class="upload-demo" ref="upload" action="" :http-request="handleUpload"  :auto-upload="false"
					 	:file-list="fileList" >
                        <el-button slot="trigger" size="medium" icon="el-icon-folder" type="primary">选取文件</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="需求分类" prop="type" hidden>
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



        <!--版本需求列表，这里是弹窗，显示所有的需求-->
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
			<el-table :data="need" ref="needTable" highlight-current-row v-loading="listLoading" @selection-change="selectionChange" style="width: 100%;">
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



         <!--版本缺陷列表，这里是弹窗，显示所有的bug-->
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
			<el-table :data="bug" ref="bugTable" highlight-current-row v-loading="listLoading" @selection-change="selectionChange" style="width: 100%;">
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
    import { getReport,getUserName,listNeed,listBug,editReport } from "../../../api/api.js";

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
                need:[],
                bug: [],
                currentneed:[],
                currentbug:[],
                selection:[],
                recipients:'',
                copiers:'',
                listNeedVisible:false,
                listBugVisible:false,
                listLoading:false,
                total:0,
                total1:0,
                iterationJson:{"1":"当前迭代","2":"后续迭代","3":"已完成迭代"},
				fileList:[],

                editForm: {
                    id:0,
                    subject: '',
                    recipient: '',
                    copier:'',
                    conclusion: '',
                    purposes: '',
					environment:'',
                    need:'',
                    bug:'',
                    useCase: '',
                    type:1,
                    isSend:''
                },
                editFormRules: {
                    subject: [{required: true, message: '请输入邮件主题', trigger: 'blur'}],
                    recipient: [{required: true, message: '请选择收件人', trigger: 'blur'}]
                },
				files:[]
            }
        },
        methods: {
        	 handleUpload(param) {
        	 	alert(param.file.name);
                this.files.push(param.file);// 一般情况下是在这里创建FormData对象，但我们需要上传多个文件，为避免发送多次请求，因此在这里只进行文件的获取，param可以拿到文件上传的所有信息
            },
            handleCancle() {
                this.$router.push('/reportforms/report/1');
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
					let arr = this.currentneed;

					this.$nextTick(() => {
					    if (arr) {
                            arr.forEach(row => {
                                this.need.forEach(need => {
                                    if (need.id==row.id){
                                        this.$refs.needTable.toggleRowSelection(need);
                                    }
                                });
                            });
                        } else {
                            this.$refs.needTable.clearSelection();
                        }
                    });
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

					let arr = this.currentbug;

					this.$nextTick(() => {
					    if (arr){
					        arr.forEach(row =>{
					            this.bug.forEach(bug => {
					                if (bug.id==row.id){
					                    this.$refs.bugTable.toggleRowSelection(bug);
                                    }
                                });
                            });
                        } else{
					        this.$refs.bugTable.clearSelection();
                        }
                    });
				});
			},
            getUsername(){
                let userParams = {};
                getUserName(userParams).then((res) => {
                    this.recipients = res.user;
                    this.copiers = res.user;
                });
            },
            //从报告中将需求移除，其实就是将report表中needs字段去掉某个id或全部id
			handleRemove: function (index) {
				this.$confirm('确认移除该记录吗?', '提示', {
					type: 'warning'
				}).then(() => {
					//this.listLoading = true;

					//这里先找出删掉的需求id，然后将总需求id减去删掉的需求id，剩下的作为para
                    let arr = this.currentneed;

                    arr.splice(index,1);//将删掉的需求去掉，arr保存的剩下的
                    this.currentneed = arr;

				}).catch(() => {

				});
			},
            //从报告中将bug移除，其实就是将report表中bugs字段去掉某个id或全部id
            handleRemove1: function (index) {
                this.$confirm('确认移除该记录吗?','提示', {
                    type: 'warning'
                }).then(() => {
                    let arr = this.currentbug;

                    arr.splice(index,1);

                    this.currentbug = arr;

                }).catch(() => {
                });
            },

            //预览邮件
            handleView(){
            	let names = "";//收件人姓名
				for (var i in this.editForm.recipient) {
					let target = this.editForm.recipient[i];

    				let obj = this.recipients.find((item)=>{
      					return item.email === target;//筛选出匹配数据
					});
    				if (names==""){
    					names = obj.loginName;
					}
    				else{
    					names = names + ";" + obj.loginName;
					}

				}
				this.editForm.names = names;

				let copier_names = "";//抄送人姓名
				for (var j in this.editForm.copier) {
					let target = this.editForm.copier[j];

    				let obj = this.copiers.find((item)=>{
      					return item.email === target;//筛选出匹配数据
					});
    				if (copier_names==""){
    					copier_names = obj.loginName;
					}
    				else{
    					copier_names = copier_names + ";" + obj.loginName;
					}

				}
				this.editForm.copier_names = copier_names;


                this.$router.push({path:'/viewTestReport',query: { editForm: this.editForm }});

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
            //编辑
            sendMail: function (isSend) {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认修改吗？', '提示', {}).then(() => {
                            this.editForm.isSend = isSend;

                            let ids = new Array();

                            for (let i in this.currentneed){
                                ids.push(this.currentneed[i].id);
                            }

                            let bug_ids = new Array();
                            for (let i in this.currentbug){
                                bug_ids.push(this.currentbug[i].id);
                            }

							this.$refs.upload.submit();

							let fileData = new FormData();
							fileData.append('id', this.editForm.id);
							fileData.append('subject', this.editForm.subject);
							fileData.append('recipient', this.editForm.recipient.join(","));
							fileData.append('copier', this.editForm.copier.join(","));
							fileData.append('conclusion', this.editForm.conclusion);
							fileData.append('purposes', this.editForm.purposes);
							fileData.append('environment', this.editForm.environment);
							fileData.append('need', ids.toString());
							fileData.append('bug', bug_ids.toString());
							fileData.append('type', this.editForm.type);

							fileData.append('isSend', this.editForm.isSend);

							this.files.forEach(function (file) {// 因为要上传多个文件，所以需要遍历
                                fileData.append('file', file);
                            });

							editReport(fileData).then((res) => {
                                 if('success'==res){
                                     this.$message({
                                         message: '修改成功',
                                         type: 'success'
                                     });
                                     this.$refs['editForm'].resetFields();
                                     this.$router.push('/reportforms/report/1');
                                 }
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

                        this.editForm=result;//这里相当于给editForm初始化了
						this.editForm.id = id;

                        this.currentneed = result.need;
                        this.currentbug = result.bug;

                        this.editForm.recipient = result.recipients.split(';');
                        this.editForm.copier = result.copiers.split(';');

						for(let f in result.files) {
							let file = {
								name:result.files[f].name,
								url:result.files[f].url,
							};
							this.fileList.push(file);
						}
                    }
                });

            },
        },
        mounted() {
            this.getUsername();
            if (this.$route.query.id) {
                this.setFormFieldValue(this.$route.query.id);
            }

        }
    }

</script>

<style scoped>

</style>
