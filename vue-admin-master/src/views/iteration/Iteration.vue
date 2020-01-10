<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item label="优先级">
                    <el-select v-model="filters.priority" clearable placeholder="请选择">
                        <el-option v-for="item in priorities" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="filters.status" clearable placeholder="请选择">
                        <el-option v-for="item in statuss" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
				<el-input v-model="filters.keyword"  size="medium" placeholder="标题/处理人" clearable style="width: 260px;"></el-input>
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
		<el-table :data="iteration" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" width="60"></el-table-column>
			<el-table-column type="index" width="60"></el-table-column>
<!--			<el-table-column prop="id" label="ID" width="100" sortable></el-table-column>-->
			<el-table-column prop="title" label="标题" width="600"></el-table-column>
			<el-table-column prop="priority" label="优先级" width="120"></el-table-column>
			<el-table-column prop="status" label="状态" width="120"></el-table-column>
			<el-table-column prop="handler" label="处理人" width="180"></el-table-column>
			<el-table-column prop="start_time" label="预计开始时间" width="140" sortable></el-table-column>
			<el-table-column prop="end_time" label="预计结束时间" width="140" sortable></el-table-column>
			<el-table-column label="操作" width="150">
				<template slot-scope="scope">
					<el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDelete(scope.row)">移除</el-button>
				</template>
			</el-table-column>
		</el-table>
		<!--工具条-->
		<div>
			<div style="float: left;">
				<el-button type="danger" @click="batchDelete" :disabled="this.sels.length==0">批量移除</el-button>
			</div>
			<div style="float: right;">
				<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="filters.currentPage"
							   :page-sizes="[10,20,30,40]" :page-size="filters.size" layout="total,sizes,prev,pager,next,jumper" :total="total">
				</el-pagination>
			</div>
		</div>

		<!--新增界面-->
		<el-dialog title="新增" v-model="listNeedVisible" :visible.sync="listNeedVisible" width="60%">
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
				<el-table-column prop="title" label="标题" width="500"></el-table-column>
				<el-table-column prop="priority" label="优先级" width="120"></el-table-column>
				<el-table-column prop="status" label="状态" width="120"></el-table-column>
				<el-table-column prop="handler" label="处理人" width="120"></el-table-column>
				<el-table-column prop="start_time" label="预计开始时间" width="170" sortable></el-table-column>
				<el-table-column prop="end_time" label="预计结束时间" width="170" sortable></el-table-column>
			</el-table>
			<!--工具条-->
			<div slot="footer" class="dialog-footer">
				<el-button size="small" type="primary" style="float: left" @click="addSubmit()" :disabled="this.selection.length==0">添加</el-button>
				<el-pagination @size-change="handleSizeChange1" @current-change="handleCurrentChange1" :current-page="filters.currentPage1"
								   :page-sizes="[10,20,30]" :page-size="filters.size1" layout="total,sizes,prev,pager,next,jumper" :total="total1">
				</el-pagination>
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
				<el-form-item label="处理人" prop="handler">
					<el-select v-model="editForm.handler" clearable placeholder="请选择">
						<el-option v-for="item in handlers" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="预计开始时间">
					<el-date-picker v-model="editForm.start_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="预计结束时间" prop="end_time">
					<el-date-picker v-model="editForm.end_time" type="date" placeholder="选择日期"></el-date-picker>
				</el-form-item>
				<el-form-item label="迭代类型" prop="type">
					<el-select v-model="editForm.type" filterable clearable placeholder="请选择">
						<el-option key="1" label="当前迭代" value=1></el-option>
						<el-option key="2" label="后续迭代" value=2></el-option>
						<el-option key="3" label="已完成迭代" value=3></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible=false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>


	</section>
</template>

<script>
	import {listIter,addIter,editIter,deleteIter,batchDeleteIter,getUserName,listNeed} from "../../api/api";
	export default {
		data(){
			return {
				filters:{
                    priority:'',
                    status:'',
					keyword:'',
					title:'',
					handler:'',
					currentPage:1,
					size:10,
					currentPage1:1,
					size1:10,
				},
				iteration:[],
				total:0,
				total1:0,
				sels:[],
				selection:[],
				need:[],
				listLoading:false,
				priorities:[{label:'高'},{label:'中'},{label:'低'}],
				statuss:[{label:'规划中'},{label:'规划完成'},{label:'评审完成'},{label:'UI设计中'},{label:'开发中'},
					{label:'提交测试'},{label:'已发布'},{label:'已拒绝'}],
				handlers:'',
				listNeedVisible:false,
				editFormVisible:false,//编辑界面是否显示
				editLoading:false,
				editFormRules:{
					title:[{ required:true,message:"请输入标题",trigger:'blur' }],
					handler:[{ required:true,message:"请选择处理人",trigger:'blur' }],
					type:[{ required:true,message:"请选择迭代类型",trigger:'blur' }],

				},
				editForm:{
					id:0,
					title:'',
					priority:'',
					handler:'',
					start_time:'',
                    end_time:'',
					type:''
				}
			}
		},
		methods:{
			search(){
				this.filters.page=1;
				this.listiter();

			},
			searchNeed(){
				this.filters.page=1;
				this.listneed();
			},
			getUsername(){
                let userParams = {};
                getUserName(userParams).then((res) => {
                    this.handlers = res.user;
                });
            },
			listiter(){
				let iterParams = {
				    priority:this.filters.priority,
                    status:this.filters.status,
					keyword:this.filters.keyword,
					page:this.filters.currentPage,
					size:this.filters.size,
					type:this.$route.params.type
				}

				this.listLoading=true;
				listIter(iterParams).then((res) => {
					this.total = res.total;
					this.iteration = res.iterationList;
					this.listLoading = false;
				});
			},
			handleAdd(){
				this.listneed();
			},
			selsChange:function(sels){
				this.sels = sels;
			},
			selectionChange:function(selection){
				this.selection = selection;
			},
			handleSizeChange(val){
				this.filters.size = val;//当前显示条数
				this.listiter();
			},
			handleSizeChange1(val){
				this.filters.size1 = val;//当前显示条数
				this.listneed();
			},

			handleCurrentChange(val){
				this.filters.currentPage = val;//当前页
				this.listiter();
			},
			handleCurrentChange1(val){
				this.filters.currentPage1 = val;//当前页
				this.listneed();
			},


			//显示编辑界面
			handleEdit:function (row){
				this.editFormVisible=true,
				this.editForm=Object.assign({},row);
				this.editForm=row;
				this.editForm.type = String(row.type);
			},

			listneed(){
				this.listNeedVisible = true;
				let needParams = {
					title:this.filters.title,
					handler:this.filters.handler,
					page:this.filters.currentPage1,
					size:this.filters.size1,
				}

				this.listLoading=true;
				listNeed(needParams).then((res) => {
					this.total1 = res.noIterTotal;
					this.need = res.noIterNeedList;
					this.listLoading = false;
				});
			},
			//将没有迭代的需求添加到迭代中
			addSubmit: function () {
				var ids = this.selection.map(item => item.id).toString();
				var type = this.$route.params.type;
				this.$confirm('确认添加吗？', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					let para = { ids : ids, type : type };
					addIter(para).then((res) => {
						this.listLoading = false;
						this.$message({
							message: '添加成功',
							type: 'success'
						});
						this.listNeedVisible=false;
						this.listiter();
					});
				}).catch(() => {

				});
			},
			//编辑
			editSubmit: function () {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							//NProgress.start();
							let para = Object.assign({}, this.editForm);
							editIter(para).then((res) => {
								this.editLoading = false;
								//NProgress.done();
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['editForm'].resetFields();
								this.editFormVisible = false;
								this.listiter();
							});
						});
					}
				});
			},

			//从迭代中移除，即不放在该迭代中
			handleDelete: function (row) {
				this.$confirm('确认移除该记录吗?', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					//NProgress.start();
					let para = { id: row.id };
					deleteIter(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '移除成功',
							type: 'success'
						});
						this.listiter();
					});
				}).catch(() => {

				});
			},
			//批量移除
			batchDelete: function () {
				var ids = this.sels.map(item => item.id).toString();
				this.$confirm('确认移除选中记录吗？', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					let para = { ids: ids };
					batchDeleteIter(para).then((res) => {
						this.listLoading = false;
						this.$message({
							message: '移除成功',
							type: 'success'
						});
						this.listiter();
					});
				}).catch(() => {

				});
			}
		},
		watch: {
            '$route' (to, from) { //监听路由是否变化
                if(this.$route.params.type){//判断id是否有值
                    Object.assign(this.$data, this.$options.data());
                    this.listiter();
                }
            }
        },
		mounted() {
			this.listiter();
			this.getUsername();
		}
	}
</script>
<style scoped>
	.el-table {
		margin-bottom: 20px;
	}
</style>