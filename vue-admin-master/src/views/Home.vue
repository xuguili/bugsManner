<template>
	<el-row class="container">
		<el-col :span="24" class="header">
			<el-col :span="10" class="logo" :class="collapsed?'logo-collapse-width':'logo-width'">
				{{collapsed?'':sysName}}
				<img v-if="collapsed" src="../assets/logo.png">
			</el-col>
			<el-col :span="10">
				<div class="tools" @click.prevent="collapse">
					<i class="fa fa-align-justify"></i>
				</div>
				<el-col :span="2" class="firstMenus" v-for="(item,index) in sysFirst" :key="index">
					<a @click="changeFirstMenu(index)" :style="index == selectFirst?'color:#ffff0c;font-size: 18px;':''">{{item.menuname}}</a>
				</el-col>
			</el-col>

			<el-col :span="4" class="userinfo">
				<el-dropdown trigger="hover">
					<span class="el-dropdown-link userinfo-inner">{{'你好，'+sysUserName}}<i class="el-icon-s-custom"></i></span>
					<el-dropdown-menu slot="dropdown">
						<el-dropdown-item @click.native="toMain()">我的消息</el-dropdown-item>
						<el-dropdown-item>设置</el-dropdown-item>
						<el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
			</el-col>
		</el-col>
		<el-col :span="24" class="main">
			<aside :class="collapsed?'menu-collapsed':'menu-expanded'">
				<!--导航菜单-->
				<el-menu :default-active="$route.path" style="overflow-y: scroll;" class="el-menu-vertical-demo" id="leftMenus" @open="handleopen" @close="handleclose" @select="handleselect"
					 unique-opened router v-show="!collapsed">
					<template v-for="(item,index) in sysMenus">
						<el-submenu :index="index+''">
							<template slot="title"><i :class="item.icon"></i>{{item.menuname}}</template>
							<el-menu-item v-for="child in item.menus" :index="child.url" :key="child.url" v-if="!child.hidden">{{child.menuname}}</el-menu-item>
						</el-submenu>
					</template>
				</el-menu>
			</aside>
			<section class="content-container">
				<div class="grid-content bg-purple-light">
					<el-col :span="24" class="breadcrumb-container">
						<el-breadcrumb separator=">" class="breadcrumb-inner">
							<el-breadcrumb-item :to="{ path: '/main' }" >
								首页
							</el-breadcrumb-item>
							<el-breadcrumb-item v-if="item.name" v-for="item in $route.matched" :to="{ path:item.path }" :key="item.path" :index="item.path">
								{{ item.name }}
							</el-breadcrumb-item>
						</el-breadcrumb>
					</el-col>
					<!--不能删,这里是其他页面的入口-->
					<el-col :span="24" class="content-wrapper">
						<transition name="fade" mode="out-in">
							<router-view></router-view>
						</transition>
					</el-col>

				</div>
			</section>
		</el-col>
	</el-row>
</template>

<script>
	export default {
		data() {
			return {
				sysName:'缺陷管理',
				collapsed:false,
				sysUserName: '',
				sysMenus:[],
				sysFirst:'',
				sysUserAvatar: '',
				selectFirst:0,
			}
		},
		methods: {
			onSubmit() {
				console.log('submit!');
			},
			handleopen() {
				//console.log('handleopen');
			},
			handleclose() {
				//console.log('handleclose');
			},
			handleselect: function (a, b) {
			},
			//退出登录
			logout: function () {
				var _this = this;
				this.$confirm('确认退出吗?', '提示', {
					//type: 'warning'
				}).then(() => {
					//requestLogout(null).then((res) => {});
					sessionStorage.removeItem('user');
					_this.$router.push('/login');
				}).catch(() => {

				});
			},
			//折叠导航栏
			collapse:function(){
				this.collapsed=!this.collapsed;
				let menuWidth = document.getElementById('leftMenus');
				menuWidth.style.width="auto";
			},
			changeFirstMenu:function (index) {
				if(this.selectFirst!=index){
					this.selectFirst = index;
					this.sysMenus = this.sysFirst[index].menus;
					this.$router.push(this.sysFirst[index].menus[0].menus[0].url);
				}

			},
			toMain(){
				this.$router.push('/main');
			}
		},
		mounted() {
			var user = sessionStorage.getItem('user');
			if (user) {
				user = JSON.parse(user);
				this.sysUserName = user.loginName || '';
				this.sysUserAvatar = user.avatar || '';
			}
			this.sysFirst = JSON.parse(user.menus);
			this.sysMenus = this.sysFirst[0].menus;
			this.$router.push('/main');

		}
	}

</script>

<style scoped lang="scss">
	@import '~scss_vars';
    .el-menu-vertical-demo:not(.el-menu--collapse) {
        min-height: 400px;
    }
	.el-menu--collapse{
		flex:0 0 60px;
		width: 60px;
		overflow-x: hidden;
	}
	.container {
		position: absolute;
		top: 0px;
		bottom: 0px;
		width: 100%;
		.header {
			height: 60px;
			line-height: 60px;
			background: $color-primary;
			color:#fff;
			.userinfo {
				text-align: right;
				padding-right: 35px;
				float: right;
				.userinfo-inner {
					cursor: pointer;
					color:#fff;
					img {
						width: 40px;
						height: 40px;
						border-radius: 20px;
						margin: 10px 0px 10px 10px;
						float: right;
					}
				}
			}
			.logo {
				//width:230px;
				height:60px;
				font-size: 22px;
				padding-left:50px;
				padding-right:20px;
				border-color: rgba(238,241,146,0.3);
				border-right-width: 1px;
				border-right-style: solid;

				.txt {
					color:#fff;
				}
			}
			.logo-width{
				width:230px;
			}
			.logo-collapse-width{
				width:60px;
                img {

                width: 50px;
                height: 50px;
                margin: 5px 0px 5px -40px;
                float: left;

            }
			}
			.tools{
				padding: 0px 23px;
                float: left;
				width:14px;
				height: 60px;
				line-height: 60px;
				cursor: pointer;
			}

            .firstMenus{
                padding: 0px 10px 0px 10px;
                float: left;
                width:auto;
                height: 60px;
                line-height: 60px;
                cursor: pointer;
				font-family: '华文楷体';
				font-size: 20px;
            }
		}
		.main {
			display: flex;
			// background: #324057;
			position: absolute;
			top: 60px;
			bottom: 0px;
			overflow: auto;
			aside {
				flex:0 0 230px;
				width: 230px;
				// position: absolute;
				// top: 0px;
				// bottom: 0px;
				.el-menu{
					height: 100%;
				}
				.collapsed{
					width:60px;
					.item{
						position: relative;
					}
					.submenu{
						position:absolute;
						top:0px;
						left:60px;
						z-index:99999;
						height:auto;
						display:none;
					}

				}
			}
			.menu-collapsed{
				flex:0 0 60px;
				width: 60px;
			}
			.menu-expanded{
				flex:0 0 230px;
				width: 230px;
			}
			.content-container {
				// background: #f1f2f7;
				flex:1;
				// position: absolute;
				// right: 0px;
				// top: 0px;
				// bottom: 0px;
				// left: 230px;
				overflow-y: scroll;
				padding: 20px;
				.breadcrumb-container {
					//margin-bottom: 15px;
					.title {
						width: 50px;
						float: left;
						height: 20px;
						color: #475669;
					}
					.breadcrumb-inner {
						height: 20px;
						float: left;
					}
				}
				.content-wrapper {
                    height: 100%;
					background-color: #fff;
					box-sizing: border-box;
				}

				.content-wrapper-down {
					background-color: #ffff0c;
					height: 30px;
				}
			}
		}
	}

</style>