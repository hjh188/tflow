#coding:utf-8
"""
App setting for tweb

We suggest you put all the app related settings here,
it's easy to maintain and good catch.

"""

from lucommon.confs import LuConf


class WebSourceConf(LuConf):
    """
    It's a good practice to write WebSource
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

    # Static File Prefix
    static_file_endpoint = 'http://127.0.0.1:8080/web/'

    default_sidebar_menu_top = ['self', 'team', 'branch', 'company']
    default_sidebar_menu_bottom = ['project', 'requirement', 'task', 'testcase',
                                   'bug', 'wiki', 'message', 'contact', 'setting']

    sidebar_menu_top_map = {
        'self': '<li id="self"><a href="index"><i class="livicon" data-name="user-flag" title="我的" data-loop="true" data-color="#42aaca" data-hc="#42aaca" data-s="25"></i></a></li>',
        'team': '<li id="team"><a href="index"><i class="livicon" data-name="users" title="团队" data-loop="true" data-color="#e9573f" data-hc="#e9573f" data-s="25"></i></a></li>',
        'branch': '<li id="branch"><a href="index"><i class="livicon" data-name="connect" title="部门" data-loop="true" data-color="#f6bb42" data-hc="#f6bb42" data-s="25"></i></a></li>',
        'company': '<li id="company"><a href="index"><i class="livicon" data-name="bank" title="公司" data-loop="true" data-color="#37bc9b" data-hc="#37bc9b" data-s="25"></i></a></li>'
    }

    # Sidebar menu bottom part
    sidebar_menu_bottom_map = {
      'project': '<li id="project"><a href="project"><i class="livicon" data-name="thumbnails-big" data-size="18" data-c="#418BCA" data-hc="#418BCA" data-loop="true"></i><span class="title">项目</span></a></li>',
      'requirement': '<li id="requirement"><a href="#"><i class="livicon" data-name="thumbnails-small" data-size="18" data-c="#00bc8c" data-hc="#00bc8c" data-loop="true"></i><span class="title">需求</span><span class="fa arrow"></span></a><ul class="sub-menu"><li><a href="index"><i class="fa fa-angle-double-right"></i>创建</a></li></ul></li>',
      'task': '<li id="task"><a href="index"><i class="livicon" data-c="#EF6F6C" data-hc="#EF6F6C" data-name="list-ul" data-size="18" data-loop="true"></i><span class="title">任务</span></a></li>',
      'testcase': '<li id="testcase"><a href="index"><i class="livicon" data-name="brush" data-c="#F89A14" data-hc="#F89A14" data-size="18" data-loop="true"></i><span class="title">测试用例</span></a></li>',
      'bug': '<li id="bug"><a href="index"><i class="livicon" data-name="bug" data-c="#5bc0de" data-hc="#5bc0de" data-size="18" data-loop="true"></i><span class="title">Bug</span></a></li>',
      'wiki': '<li id="wiki"><a href="index"><i class="livicon" data-name="doc-portrait" data-c="#5bc0de" data-hc="#5bc0de" data-size="18" data-loop="true"></i><span class="title">文档</span></a></li>',
      'message': '<li id="message"><a href="index"><i class="livicon" data-name="comment" data-c="#F89A14" data-hc="#F89A14" data-size="18" data-loop="true"></i><span class="title">消息</span></a></li>',
      'contact': '<li id="contact"><a href="index"><i class="livicon" data-name="share" data-size="18" data-c="#00bc8c" data-hc="#00bc8c" data-loop="true"></i><span class="title">通讯录</span></a></li>',
      'setting': '<li id="setting"><a href="index"><i class="livicon" data-name="hammer" data-c="#418bca" data-hc="#418bca" data-size="18" data-loop="true"></i><span class="title">配置</span></a></li>'
    }

    base_resp_context = {
        'static_file_endpoint': static_file_endpoint,
    }

