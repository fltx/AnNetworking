#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os;

class xxnetos(object):

    @classmethod
    def mkdir(cls,path):
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
           # 如果不存在则创建目录
           # 创建目录操作函数
            os.makedirs(path)

            print path + ' 创建成功'
            return True
        else:
           # 如果目录存在则不创建，并提示目录已存在
            print path + ' 目录已存在'
            return False


    @classmethod
    def mkfile(cls,folder,name, content):
        filepath = folder.rstrip("//") + "/" + name
        fd = open(filepath, 'w')
        fd.write(content)
        fd.close()  # 操作完文件后一定要记得关闭，释放内存资源


    @classmethod
    def mkclass(cls,h_content, m_content, filename, module,replace,folder):
        h_content = h_content.replace(replace, module);
        m_content = m_content.replace(replace, module);
        filename = filename.replace(replace, module);

        xxnetos.mkfile(folder, filename + ".h", h_content);
        xxnetos.mkfile(folder, filename + ".m", m_content);



    @classmethod
    def mkdefines(cls,content, filename, module,replace,folder):
        content = content.replace(replace, module);
        filename = filename.replace(replace, module);

        xxnetos.mkfile(folder, filename + ".h", content);
