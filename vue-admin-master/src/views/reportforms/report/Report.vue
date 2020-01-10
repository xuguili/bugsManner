<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
                <el-form-item>
				<el-input v-model="filters.keyword"  size="medium" placeholder="报告名称/创建人" clearable style="width: 260px;"></el-input>
				</el-form-item>
                <el-form-item label="发送时间">
                    <el-date-picker type="date" v-model="filters.sendTime" placeholder="选择日期">
                    </el-date-picker>
                </el-form-item>
				<el-form-item>
					<el-button type="primary" size="small" icon="el-icon-search" v-on:click="search">搜索</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="small" icon="el-icon-plus" v-on:click="handleAdd">创建</el-button>
				</el-form-item>
			</el-form>
		</el-col>
		<!--列表-->
		<el-table :data="report" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" width="60"></el-table-column>
			<el-table-column type="index" width="60"></el-table-column>
<!--			<el-table-column prop="id" label="ID" width="100" sortable></el-table-column>-->
			<el-table-column prop="subject" label="报告名称" width="600"></el-table-column>
            <el-table-column prop="status" label="状态" width="140"></el-table-column>
			<el-table-column prop="sendTime" label="发送时间" width="140"></el-table-column>
			<el-table-column prop="type" label="报告类型" :formatter="formatType" width="140"></el-table-column>
			<el-table-column prop="creater" label="创建人" width="140" sortable></el-table-column>
			<el-table-column label="操作" width="400">
				<template slot-scope="scope">
                    <el-button type="primary" size="small" @click="handleView(scope.row)">查看</el-button>
					<el-button type="primary" size="small" @click="handleEdit(scope.row)" :disabled="scope.row.status=='已发送'">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
		<!--工具条-->
		<div>
			<div style="float: left;">
				<el-button type="danger" @click="batchDelete" :disabled="this.sels.length==0">批量删除</el-button>
			</div>
			<div style="float: right;">
				<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="filters.currentPage"
							   :page-sizes="[10,20,50,100]" :page-size="filters.size" layout="total,sizes,prev,pager,next,jumper" :total="total">
				</el-pagination>
			</div>
		</div>

	</section>
</template>

<script>
	import { listReport,deleteReport,batchDeleteReport } from "../../../api/api.js";
	import util from "../../../common/js/util.js";

	export default {
		data(){
			return {
				filters:{
					keyword:'',
					sendTime:'',
					currentPage:1,
					size:10,
				},
				report:[],
				total:0,
				sels:[],
				listLoading:false,
                typeJson:{"1":"测试报告","2":"发布报告"}

			}
		},
		methods:{
			search(){
				this.filters.page=1;
				this.listreport();
			},
            formatType(row){
			    //将类型格式化
			    if(row.type){
			        return this.typeJson[row.type];
                }
            },
			listreport(){
				let reportParams = {
					keyword:this.filters.keyword,
					sendTime:this.filters.sendTime ? util.formatDate.format(new Date(this.filters.sendTime),'yyyy-MM-dd') : '',
					page:this.filters.currentPage,
					size:this.filters.size,
					type:this.$route.params.type
				}

				this.listLoading=true;
				listReport(reportParams).then((res) => {
					this.total = res.total;
					this.report = res.reportList;
					this.listLoading = false;
				});
			},
			handleAdd(){
				if(this.$route.params.type ==1)
				{
					this.$router.push('/addTestReport');
				}
				else{
					this.$router.push('/addReleaseReport');
				}
			},
			handleEdit(row){
				if (this.$route.params.type ==1)
				{
					this.$router.push({path:'/editTestReport',query: { id: row.id }});
				}
				else{
					this.$router.push({path:'/editReleaseReport',query: { id: row.id }});
				}

            },
			handleView(row){
				if (this.$route.params.type ==1)
				{
					this.$router.push({path:'/viewTestReport',query: { id: row.id }});
				}
				else{
					this.$router.push({path:'/viewReleaseReport',query: { id: row.id }});
				}

            },
			selsChange:function(sels){
				this.sels = sels;
			},
			handleSizeChange(val){
				this.filters.size = val;//当前显示条数
				this.listreport();
			},
			handleCurrentChange(val){
				this.filters.currentPage = val;//当前页
				this.listreport();
			},
			//删除
			handleDelete: function (row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					//NProgress.start();
					let para = { id: row.id };
					deleteReport(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listreport();
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
					batchDeleteReport(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listreport();
					});
				}).catch(() => {

				});
			}
		},
		watch: {
            '$route' (to, from) { //监听路由是否变化
                if(this.$route.params.type){//判断id是否有值
                    Object.assign(this.$data, this.$options.data());
                    this.listreport();
                }
            }
        },
		mounted() {
			this.listreport();
		}
	}
</script>
<style scoped>
	.el-table {
		margin-bottom: 20px;
	}
</style>