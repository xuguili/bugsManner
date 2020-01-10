<template>
	<section>
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
					<el-button type="primary" size="medium" icon="el-icon-search" v-on:click="search">搜索</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="medium" icon="el-icon-plus" v-on:click="handleAdd">新增</el-button>
				</el-form-item>
			</el-form>
		</el-col>
		<!--列表-->
		<el-table :data="need" highlight-current-row v-loading="listLoading" @selection-change="selsChange"  style="width: 100%;">
			<el-table-column type="selection" width="60"></el-table-column>
			<el-table-column type="index" width="60"></el-table-column>
<!--			<el-table-column prop="id" label="ID" width="100" sortable></el-table-column>-->
			<el-table-column prop="title" label="标题" width="500"></el-table-column>
			<el-table-column prop="priority" label="优先级" width="100"></el-table-column>
			<el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="100"></el-table-column>
			<el-table-column prop="status" label="状态" width="100">
				 <template scope="scope"><i class="el-icon-edit" @click="handleUpdate(scope.row)"></i>{{scope.row.status}}</template>
			</el-table-column>
			<el-table-column prop="handler" label="处理人" width="150"></el-table-column>
			<el-table-column prop="start_time" label="预计开始时间" width="150" sortable></el-table-column>
			<el-table-column prop="end_time" label="预计结束时间" width="150" sortable></el-table-column>
			<el-table-column label="操作" width="150">
				<template slot-scope="scope">
					<el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
		<!--工具条-->
		<div>
			<div style="float: left;">
				<el-button type="danger" @click="batchDelete" :disabled="this.sels.length==0">批量删除</el-button>
				 <el-button type="primary" @click="batchHandleUpdate()" :disabled= "noBatch">批量处理</el-button>
			</div>
			<div style="float: right;">
				<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="filters.currentPage"
							   :page-sizes="[10,20,50,100]" :page-size="filters.size" layout="total,sizes,prev,pager,next,jumper" :total="total">
				</el-pagination>
			</div>
		</div>

		<!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :visible.sync="addFormVisible" width="50%">
			<el-form :model="addForm" label-position="right" label-width="80px"  :rules="addFormRules" ref="addForm">
				<el-form-item label="标题" prop="title" style="width: 50%;">
					<el-input v-model="addForm.title" clearable auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="优先级">
					<el-select v-model="addForm.priority" clearable placeholder="请选择">
						<el-option v-for="item in priorities" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="迭代">
					<el-select v-model="addForm.iteration" clearable placeholder="请选择">
						<el-option key="1" label="当前迭代" value=1></el-option>
						<el-option key="2" label="后续迭代" value=2></el-option>
						<el-option key="3" label="已完成迭代" value=3></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="处理人" prop="handler">
					<el-select v-model="addForm.handler"  multiple  clearable placeholder="请选择">
						<el-option v-for="item in handlers" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="预计开始时间">
					<el-date-picker v-model="addForm.start_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="预计结束时间" prop="end_time">
					<el-date-picker v-model="addForm.end_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="需求分类" prop="type">
					<el-select v-model="addForm.type" filterable clearable placeholder="请选择">
						<el-option key="1" label="产品需求" value=1></el-option>
						<el-option key="2" label="运营需求" value=2></el-option>
						<el-option key="3" label="设计需求" value=3></el-option>
						<el-option key="4" label="技术需求" value=4></el-option>
					</el-select>
				</el-form-item>

			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible=false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :visible.sync="editFormVisible">
			<el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
				<el-form-item label="标题" prop="title">
					<el-input v-model="editForm.title" clearable auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="优先级">
					<el-select v-model="editForm.priority" clearable placeholder="请选择">
						<el-option v-for="item in priorities" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="迭代">
					<el-select v-model="editForm.iteration" filterable clearable placeholder="请选择">
						<el-option key="1" label="当前迭代" value=1></el-option>
						<el-option key="2" label="后续迭代" value=2></el-option>
						<el-option key="3" label="已完成迭代" value=3></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="处理人" prop="handler">
					<el-select v-model="editForm.handler" multiple clearable placeholder="请选择">
						<el-option v-for="item in handlers" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="预计开始时间">
					<el-date-picker v-model="editForm.start_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="预计结束时间" prop="end_time">
					<el-date-picker v-model="editForm.end_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="需求分类" prop="type">
					<el-select v-model="editForm.type" filterable clearable placeholder="请选择">
						<el-option label="产品需求" value=1></el-option>
						<el-option label="运营需求" value=2></el-option>
						<el-option label="设计需求" value=3></el-option>
						<el-option label="技术需求" value=4></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible=false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--编辑状态-->
		<el-dialog title="编辑状态" v-model="updateFormVisible" :visible.sync="updateFormVisible">
			<el-form :model="updateForm" label-width="100px"  ref="updateForm">
                <el-container>
                    <div width="200px" style="background:#eff0f4">
                        <div v-if="updateForm.status=='规划中'">
                           <ul>
                                <li class="div-left"><el-radio v-model="radio" label="规划完成">规划完成</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>

                        </div>
                         <div v-else-if="updateForm.status=='规划完成'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="评审完成">评审完成</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="规划中">规划中</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='评审完成'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="UI设计中">UI设计中</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="开发中">开发中</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='UI设计中'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="开发中">开发中</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='开发中'">
                            <li class="div-left"><el-radio v-model="radio" label="提交测试">提交测试</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
                        <div v-else-if="updateForm.status=='已发布'">
                            <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
						<div v-else-if="updateForm.status=='提交测试'">
                            <li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
                    </div>
                    <div style="width:770px; background-color:#FAFAFA;height: 400px;padding: 20px 20px 0px 20px">
                        <el-form-item label="处理人" prop="handler" style="width: 400px">
                            <el-input v-model="updateForm.handler" clearable></el-input>
                        </el-form-item>
<!--                        <el-form-item label="评论" style="width: 400px">-->
<!--                            <el-input  style="height: 220px" placeholder="@通知他人，增加评论/处理意见" clearable></el-input>-->
<!--                        </el-form-item>-->
                    </div>
                </el-container>

			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="updateFormVisible=false">取消</el-button>
				<el-button type="primary" @click.native="updateSubmit" :loading="updateLoading">确定</el-button>
			</div>
		</el-dialog>


		  <!--批量处理-->
		<el-dialog title="批量处理" v-model="batchUpdateFormVisible" :visible.sync="batchUpdateFormVisible">
			<el-form :model="batchUpdateForm" label-width="100px"  ref="batchUpdateForm">
                <el-container>
                    <div width="200px" style="background:#eff0f4">
                        <div v-if="batchUpdateForm.status=='规划中'">
                           <ul>
                                <li class="div-left"><el-radio v-model="radio" label="规划完成">规划完成</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>

                        </div>
                         <div v-else-if="updateForm.status=='规划完成'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="评审完成">评审完成</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="规划中">规划中</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='评审完成'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="UI设计中">UI设计中</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="开发中">开发中</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='UI设计中'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="开发中">开发中</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
								<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='开发中'">
                            <li class="div-left"><el-radio v-model="radio" label="提交测试">提交测试</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='已发布'">
                            <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
						<div v-else-if="batchUpdateForm.status=='提交测试'">
                            <li class="div-left"><el-radio v-model="radio" label="已发布">已发布</el-radio></li>
							<li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                        </div>
                    </div>
                    <div style="width:770px; background-color:#FAFAFA;height: 400px;padding: 20px 20px 0px 20px">
                        <el-form-item label="处理人" prop="handler" style="width: 400px">
                            <el-input v-model="batchUpdateForm.handler" clearable></el-input>
                        </el-form-item>
<!--                        <el-form-item label="评论" style="width: 400px">-->
<!--                            <el-input  style="height: 220px" placeholder="@通知他人，增加评论/处理意见" clearable></el-input>-->
<!--                        </el-form-item>-->
                    </div>
                </el-container>

			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="batchUpdateFormVisible=false">取消</el-button>
				<el-button type="primary" @click.native="batchUpdateSubmit" :loading="batchUpdateLoading">确定</el-button>
			</div>
		</el-dialog>


	</section>
</template>

<script>
	import {listNeed,addNeed,editNeed,deleteNeed,batchDeleteNeed,getUserName} from "../../api/api";
	export default {
		data(){
			return {
				filters:{
					title:'',
					handler:'',
					currentPage:1,
					size:10,
				},

				iterationJson:{"1":"当前迭代","2":"后续迭代","3":"已完成迭代"},
				need:[],
				total:0,
				sels:[],
				radio:'1',
				noBatch:true,
				listLoading:false,
				priorities:[{label:'高'},{label:'中'},{label:'低'}],
				handlers:'',
				value:'',
				addFormVisible:false,//新增界面是否显示
				addLoading:false,
				addFormRules:{
					title:[{ required:true,message:"请输入标题",trigger:'blur' }],
					handler:[{ required:true,message:"请选择处理人",trigger:'blur' }],
					type:[{ required:true,message:"请选择需求分类",trigger:'blur' }]

				},
				//新增界面数据
				addForm:{
					id:0,
					title:'',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					start_time:'',
					end_time:'',
					type:'',
				},

				editFormVisible:false,//编辑界面是否显示
				editLoading:false,
				editFormRules:{
					title:[{ required:true,message:"请输入标题",trigger:'blur' }],
					handler:[{ required:true,message:"请选择处理人",trigger:'blur' }],
					type:[{ required:true,message:"请选择需求分类",trigger:'blur' }]
				},
				editForm:{
					ids:0,
					title:'',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					start_time:'',
					end_time:'',
					type:'',
				},
				updateFormVisible:false,
                updateLoading:false,
                updateForm:{
				    ids:'',
				    status:'',
                    handler:''
                },
                batchUpdateFormVisible:false,
                batchUpdateLoading:false,
                batchUpdateForm:{
				    ids:[],
				    status:'',
                    handler:''
                },

			}
		},
		methods:{
			search(){
				this.filters.page=1;
				this.listneed();
			},
			//将迭代格式化，数字转成文字
			formatIteration(row){
				if(row.iteration){
					return this.iterationJson[row.iteration];
				}
			},
			getUsername(){
                let userParams = {};
                getUserName(userParams).then((res) => {
                    this.handlers = res.user;
                });
            },
			//控制批量处理按钮是否可见
            isAble(){
                if(this.sels.length==0){
                    this.noBatch = true;
                    return;
                } else {
                    for (let i in this.sels) {
                        if (this.sels[0].status != this.sels[i].status) {
                            this.noBatch =  true;
                            return;
                        }
                        if (this.sels[0].handler != this.sels[i].handler) {
                            this.noBatch =  true;
                            return;
                        }
                    }
                     this.noBatch =  false;
                }
            },
			listneed(){
				let needParams = {
					title:this.filters.title,
					handler:this.filters.handler,
					page:this.filters.currentPage,
					size:this.filters.size,
					type:this.$route.params.type
				}

				this.listLoading=true;
				listNeed(needParams).then((res) => {
					this.total = res.total;
					this.need = res.needList;
					this.listLoading = false;
				});
			},
			handleAdd(){
				this.$router.push('/addNeed')
			},
			selsChange:function(sels){
				this.sels = sels;
				this.isAble();
			},
			handleSizeChange(val){
				this.filters.size = val;//当前显示条数
				this.listneed();
			},
			handleCurrentChange(val){
				this.filters.currentPage = val;//当前页
				this.listneed();
			},
			//显示新增界面
			handleAdd: function () {
				this.addFormVisible = true;
				this.addForm = {
					title: '',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					start_time:'',
					end_time:'',
					type:''
				};
			},
			//显示编辑界面
			handleEdit:function (row){
				this.editFormVisible=true,
				this.editForm=Object.assign({},row);

				this.editForm=row;
				this.editForm.ids = row.id;
				this.editForm.type = String(row.type);
				this.editForm.handler = row.handler.split(';');
			},
			 //显示编辑状态界面
            handleUpdate:function(row){
                this.updateFormVisible=true;
                this.radio = '';
                this.updateForm={
				    ids:row.id,
				    status:row.status,
                    handler:row.handler
                };
            },

            //显示批量处理弹窗
             batchHandleUpdate:function(){
                this.batchUpdateFormVisible=true;
                this.radio = '';
                let ids = this.sels.map(item => item.id).toString();
                let status = this.sels[0].status;
                let handler = this.sels[0].handler;
                this.batchUpdateForm={
				    ids:ids,
				    status:status,
                    handler:handler
                };
            },

            //编辑状态
            updateSubmit:function(){
                this.$refs.updateForm.validate((valid) => {
                    if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.updateLoading = true;
							this.updateForm.status = this.radio;
							let para = Object.assign({}, this.updateForm);

							editNeed(para).then((res) => {
								this.updateLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['updateForm'].resetFields();
								this.updateFormVisible = false;
								this.listneed();
							});
						});
					}
				});

            },
			 //批量修改状态
            batchUpdateSubmit: function () {
                this.$refs.batchUpdateForm.validate((valid) => {
                    if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.batchUpdateLoading = true;
							this.batchUpdateForm.status = this.radio;
							let para = Object.assign({}, this.batchUpdateForm);
							editNeed(para).then((res) => {
								this.batchUpdateLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['batchUpdateForm'].resetFields();
								this.batchUpdateFormVisible = false;
								this.listneed();
							});
						});
					}
				});
			},
			//新增
			addSubmit:function(){
				this.$refs.addForm.validate((valid) =>{
						if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.addLoading = true;
							let handler = this.addForm.handler[0];
							for (let i = 1; i < this.addForm.handler.length; i++) {
								handler = handler+";"+this.addForm.handler[i];
							}
							this.addForm.handler = handler;
							let para = Object.assign({}, this.addForm);

							addNeed(para).then((res) => {
								this.addLoading = false;

								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['addForm'].resetFields();
								this.addFormVisible = false;
								this.listneed();
							});
						});
					}

				});
			},
			//编辑
			editSubmit: function () {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							let handler = this.editForm.handler[0];
							for (let i = 1; i < this.editForm.handler.length; i++) {
								handler = handler+";"+this.editForm.handler[i];
							}
							this.editForm.handler = handler;
							let para = Object.assign({}, this.editForm);
							editNeed(para).then((res) => {
								this.editLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['editForm'].resetFields();
								this.editFormVisible = false;
								this.listneed();
							});
						});
					}
				});
			},

			//删除
			handleDelete: function (row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					//NProgress.start();
					let para = { id: row.id };
					deleteNeed(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listneed();
					});
				}).catch(() => {

				});
			},
			//批量删除
			batchDelete: function () {
				var ids = this.sels.map(item => item.id).toString();
				this.$confirm('确认删除选中记录吗？', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					//NProgress.start();
					let para = { ids: ids };
					batchDeleteNeed(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listneed();
					});
				}).catch(() => {

				});
			}
		},

		watch: {
            '$route' (to, from) { //监听路由是否变化
                if(this.$route.params.type){//判断id是否有值
                    Object.assign(this.$data, this.$options.data());
                    this.listneed();
                }
            }
        },
		mounted() {
			this.listneed();
			this.getUsername();
		}
	}
</script>
<style scoped>
	.el-table {
		margin-bottom: 20px;
	}

    .div-left{
        height: 50px;
        list-style:none;
        padding:20px 20px 0px 20px;
    }

</style>