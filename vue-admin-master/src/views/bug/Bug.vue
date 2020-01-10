<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item label="严重程度">
                    <el-select v-model="filters.severity" clearable placeholder="请选择">
                        <el-option v-for="item in severities" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="filters.status" clearable placeholder="请选择">
                        <el-option v-for="item in statuss" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="创建时间">
                        <el-date-picker v-model="filters.startDate" type="date" placeholder="开始日期"
                                        :options="startDateOption" @on-change="onStartDateChange">
                        </el-date-picker>
						<el-form-item label="--"></el-form-item>
                        <el-date-picker v-model="filters.endDate" type="date" placeholder="结束日期"
                        :options="endDateOption" @on-change="onEndDateChange">
                        </el-date-picker>
                </el-form-item>
                <el-form-item>
				<el-input v-model="filters.keyword"  size="medium" placeholder="标题/处理人/创建人" clearable style="width: 260px;"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="small" icon="el-icon-search" v-on:click="search">搜索</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" size="small" icon="el-icon-plus" v-on:click="handleAdd">新增</el-button>
				</el-form-item>
			</el-form>
		</el-col>
		<!--列表-->
		<el-table :data="bug" highlight-current-row v-loading="listLoading" @selection-change="selsChange"  style="width: 100%;">
			<el-table-column type="selection" width="60"></el-table-column>
			<el-table-column type="index" width="60"></el-table-column>
<!--			<el-table-column prop="id" label="ID" width="100" sortable></el-table-column>-->
			<el-table-column prop="title" label="标题" width="500"></el-table-column>
            <el-table-column prop="severity" label="严重程度" width="110"></el-table-column>
			<el-table-column prop="priority" label="优先级" width="100"></el-table-column>
			<el-table-column prop="iteration" label="迭代" :formatter="formatIteration" width="110"></el-table-column>
			<el-table-column prop="status"  label="状态" width="110">
                <template scope="scope"><i class="el-icon-edit" @click="handleUpdate(scope.row)"></i>{{scope.row.status}}</template>
            </el-table-column>
			<el-table-column prop="handler" label="处理人" width="150"></el-table-column>
			<el-table-column prop="creater" label="创建人" width="110" sortable></el-table-column>
			<el-table-column prop="createTime" label="创建时间" width="150" sortable></el-table-column>
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
                <el-form-item label="严重程度" prop="severity">
					<el-select v-model="addForm.severity" filterable clearable placeholder="请选择">
						<el-option v-for="item in severities" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
					</el-select>
                </el-form-item>
				<el-form-item label="优先级">
					<el-select v-model="addForm.priority" clearable placeholder="请选择">
						<el-option v-for="item in options1" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="迭代">
					<el-select v-model="addForm.iteration" clearable placeholder="请选择">
						<el-option key="1" label="当前迭代" value=1></el-option>
						<el-option key="2" label="后续迭代" value=2></el-option>
						<el-option key="3" label="已完成迭代" value=3></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="状态" prop="status" hidden>
					<el-select v-model="addForm.status" clearable placeholder="请选择">
						<el-option v-for="item in statuss" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="处理人" prop="handler" >
					<el-select v-model="addForm.handler" multiple clearable placeholder="请选择">
						<el-option v-for="item in handlers" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
                <el-form-item label="缺陷类型" prop="type">
					<el-select v-model="addForm.type" filterable clearable placeholder="请选择">
						<el-option label="缺陷列表" value=1></el-option>
						<el-option label="缺陷池" value=2></el-option>
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
				<el-form-item label="标题" prop="title" style="width: 500px;">
					<el-input v-model="editForm.title" clearable auto-complete="off"></el-input>
				</el-form-item>
                <el-form-item label="严重程度" prop="severity">
					<el-select v-model="editForm.severity" filterable clearable placeholder="请选择">
						<el-option v-for="item in severities" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
					</el-select>
                </el-form-item>
				<el-form-item label="优先级">
					<el-select v-model="editForm.priority" clearable placeholder="请选择">
						<el-option v-for="item in options1" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="迭代">
					<el-select v-model="editForm.iteration" clearable placeholder="请选择">
						<el-option key="1" label="当前迭代" value=1></el-option>
						<el-option key="2" label="后续迭代" value=2></el-option>
						<el-option key="3" label="已完成迭代" value=3></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="状态" prop="status" hidden>
					<el-select v-model="editForm.status" clearable placeholder="请选择">
						<el-option v-for="item in statuss" :label="item.label" :key="item.label" :value="item.label"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="处理人" prop="handler">
					<el-select v-model="editForm.handler" multiple  clearable placeholder="请选择">
						<el-option v-for="item in handlers" :label="item['loginName']" :key="item['loginName']" :value="item['loginName']"></el-option>
					</el-select>
				</el-form-item>
                <el-form-item label="缺陷类型" prop="type">
					<el-select v-model="editForm.type" filterable clearable placeholder="请选择">
						<el-option label="缺陷列表" value=1></el-option>
						<el-option label="缺陷池" value=2></el-option>
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
                        <div v-if="updateForm.status=='新' || updateForm.status=='重新打开'">
                           <ul>
                                <li class="div-left"><el-radio v-model="radio" label="接受/处理">接受/处理</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="挂起">挂起</el-radio></li>
                            </ul>

                        </div>
                        <div v-else-if="updateForm.status=='接受/处理'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已解决">已解决</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='已解决'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已验证">已验证</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='已验证' || updateForm.status=='已拒绝'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已关闭">已关闭</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="updateForm.status=='已关闭'">
                            <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                        </div>
                        <div v-else>
                            <li class="div-left"><el-radio v-model="radio" label="接受/处理">接受/处理</el-radio></li>
                            <li class="div-left"><el-radio v-model="radio" label="已解决">已解决</el-radio></li>
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
                        <div v-if="batchUpdateForm.status=='新' || batchUpdateForm.status=='重新打开'">
                           <ul>
                                <li class="div-left"><el-radio v-model="radio" label="接受/处理">接受/处理</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="挂起">挂起</el-radio></li>
                            </ul>

                        </div>
                        <div v-else-if="batchUpdateForm.status=='接受/处理'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已解决">已解决</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="已拒绝">已拒绝</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='已解决'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已验证">已验证</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='已验证' || batchUpdateForm.status=='已拒绝'">
                            <ul>
                                <li class="div-left"><el-radio v-model="radio" label="已关闭">已关闭</el-radio></li>
                                <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                            </ul>
                        </div>
                        <div v-else-if="batchUpdateForm.status=='已关闭'">
                            <li class="div-left"><el-radio v-model="radio" label="重新打开">重新打开</el-radio></li>
                        </div>
                        <div v-else>
                            <li class="div-left"><el-radio v-model="radio" label="接受/处理">接受/处理</el-radio></li>
                            <li class="div-left"><el-radio v-model="radio" label="已解决">已解决</el-radio></li>
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
	import {listBug,addBug,editBug,deleteBug,batchDeleteBug,getUserName} from "../../api/api";
	import util from '../../common/js/util.js';
	export default {
		data(){
			return {
				filters:{
					keyword:'',
					severity:'',
                    status:'',
                    startDate:'',
                    endDate:'',
					currentPage:1,
					size:10,
				},
				iterationJson:{"1":"当前迭代","2":"后续迭代","3":"已完成迭代"},
                startDateOption:{},
                endDateOption:{},
                radio:'1',
				bug:[],
				total:0,
				sels:[],
                noBatch:true,
				listLoading:false,
                severities:[{label:"致命"},{label:"严重"},{label:"一般"},{label:"提示"},{label:"建议"}],
				options1:[{label:'紧急'},{label:'高'},{label:'中'},{label:'低'},{label:'无关紧要'}],
				options2:[{label:'后续迭代'},{label:'当前迭代'},{label:'已完成迭代'}],
				statuss:[{label:'新'},{label:'接受/处理'},{label:'重新打开'},{label:'已解决'},{label:'已验证'},{label:'已关闭'},{label:'挂起'}],
				handlers:'',
				addFormVisible:false,//新增界面是否显示
				addLoading:false,
				addFormRules:{
					title:[{ required:true,message:"请输入标题",trigger:'blur' }],
                    severity:[{ required:true,message:"请选择严重程度",trigger:'blur' }],
					handler:[{ required:true,message:"请选择处理人",trigger:'blur' }],
					type:[{ required:true,message:"请选择缺陷类型",trigger:'blur' }]

				},
				//新增界面数据
				addForm:{
					id:0,
					title:'',
                    severity:'',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					createTime:'',
                    type:''
				},
				editFormVisible:false,//编辑界面是否显示
				editLoading:false,
				editFormRules:{
					title:[{ required:true,message:"请输入标题",trigger:'blur' }],
                    severity:[{ required:true,message:"请选择严重程度",trigger:'blur' }],
					handler:[{ required:true,message:"请选择处理人",trigger:'blur' }],
					type:[{ required:true,message:"请选择缺陷类型",trigger:'blur' }]
				},
                //编辑界面数据
				editForm:{
					ids:0,
					title:'',
                    severity:'',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					createTime:'',
					type:''
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
		     onStartDateChange(startDate, type) {
                     this.endDateOption = {
                         disabledDate(endDate) {
                             return endDate < new Date(startDate) || endDate > Date.now()
                         }
                     }
                 },
                 /**
                  * 结束时间发生变化时触发,设置开始时间不可选择的日期
                  * 开始时间小于等于结束时间,且小于等于当前时间
                  * @param {string} date 格式化后的日期
                  * @param {string} type 当前的日期类型
                  */
                 onEndDateChange(endDate, type) {
                    this.startDateOption = {
                        disabledDate(startDate) {
                             return startDate > new Date(endDate) || startDate > Date.now()
                         }
                     }
                 },
			//将迭代格式化，数字转成文字
			formatIteration(row){
				if(row.iteration){
					return this.iterationJson[row.iteration];
				}
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
                    }

                    let handlerArr = new Array();
                    let iseq = true;
                	handlerArr = this.sels[0].handler.split(";");
                	alert(handlerArr);
					for (let j in handlerArr) {
						iseq = true;
						for (let i in this.sels) {
							let handlerTar = this.sels[i].handler.split(";");
							if (handlerTar.indexOf(handlerArr[j])<0) {
								iseq = false;
							}
						}
						if (iseq){
							break;
						}
					}
					this.noBatch =  false;
                }
            },


			search(){
				this.filters.page=1;
				this.listbug();
			},

			listbug(){
				let bugParams = {
					keyword:this.filters.keyword,
					severity:this.filters.severity,
                    status:this.filters.status,
                    startDate:this.filters.startDate ? util.formatDate.format(new Date(this.filters.startDate), 'yyyy-MM-dd'):'',
                    endDate:this.filters.endDate ? util.formatDate.format(new Date(this.filters.endDate), 'yyyy-MM-dd'):'',
					page:this.filters.currentPage,
					size:this.filters.size,
					type:this.$route.params.type
				}

				this.listLoading=true;
				listBug(bugParams).then((res) => {
					this.total = res.total;
					this.bug = res.bugList;
					this.listLoading = false;
				});
			},
			getUsername(){
                let userParams = {}
                getUserName(userParams).then((res) => {
                    this.handlers = res.user;
                });
            },

			handleAdd(){
				this.$router.push('/addBug')
			},
			selsChange:function(sels){
				this.sels = sels;
				this.isAble();
			},
			handleSizeChange(val){
				this.filters.size = val;//当前显示条数
				this.listbug();
			},
			handleCurrentChange(val){
				this.filters.currentPage = val;//当前页
				this.listbug();
			},
			//显示新增界面
			handleAdd: function () {
				this.addFormVisible = true;
				this.addForm = {
					title: '',
                    severity:'',
					priority:'',
					iteration:'',
					status:'',
					handler:'',
					createTime:'',
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
                            para.createTime = (!para.createTime || para.createTime == '') ? '' : util.formatDate.format(new Date(para.createTime), 'yyyy-MM-dd');
							addBug(para).then((res) => {
								this.addLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['addForm'].resetFields();
								this.addFormVisible = false;
								this.listbug();
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
							editBug(para).then((res) => {
								this.editLoading = false;
								//NProgress.done();
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['editForm'].resetFields();
								this.editFormVisible = false;
								this.listbug();
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
					deleteBug(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listbug();
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
					batchDeleteBug(para).then((res) => {
						this.listLoading = false;
						//NProgress.done();
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listbug();
					});
				}).catch(() => {

				});
            },
            //编辑状态
            updateSubmit:function(){
                this.$refs.updateForm.validate((valid) => {
                    if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.updateLoading = true;
							this.updateForm.status = this.radio;
							let para = Object.assign({}, this.updateForm);
							editBug(para).then((res) => {
								this.updateLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['updateForm'].resetFields();
								this.updateFormVisible = false;
								this.listbug();
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
							editBug(para).then((res) => {
								this.batchUpdateLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								});
								this.$refs['batchUpdateForm'].resetFields();
								this.batchUpdateFormVisible = false;
								this.listbug();
							});
						});
					}
				});
			}
		},
		watch: {
            '$route' (to, from) { //监听路由是否变化
                if(this.$route.params.type){//判断id是否有值
                    Object.assign(this.$data, this.$options.data());
                    this.listbug();
                }
            }
        },
		mounted() {
			this.listbug();
			this.startDate = '2019-09-01';
            this.endDate = '2019-10-01';
            this.onStartDateChange(this.startDate);
            this.onEndDateChange(this.endDate)
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