#!/usr/bin/env python3
"""Trang cá nhân Aaron. Tĩnh, song ngữ (vi mặc định ở gốc, en trong /en/).
Thêm nội dung: thêm một mục vào WORK / PUBS / JOURNEY / NOTES rồi chạy `python3 build.py`.
Mục có "star": True sẽ tự nổi lên (trang chủ lấy mục WORK có star đầu tiên)."""
import os, html, json
ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape
EMAIL = 'aaron89.workplace@gmail.com'
ME = '<b>N. N. G. Ninh</b>'

T = {  # chuỗi giao diện
 'vi': dict(home='Trang chủ', journey='Hành trình', work='Nghiên cứu', pubs='Công bố', about='Giới thiệu', notes='Ghi chép',
            slogan='Công nghệ chỉ có nghĩa khi <em>đến được với con người.</em>', slogan_plain='Công nghệ chỉ có nghĩa khi đến được với con người.',
            who='Tôi là <b>Nguyễn Ngọc Gia Ninh</b>, thường gọi là Aaron, nghiên cứu viên AI tại GREEN-X, VinUniversity. Tôi xây dữ liệu và hệ thống thị giác máy tính cho những bài toán gần với con người: trước là người bệnh, nay là biển.',
            hello='Xin chào, tôi là', name='Nguyễn Ngọc<br>Gia Ninh', myrole='Trợ lý nghiên cứu · GREEN-X, VinUniversity', words=['trí tuệ nhân tạo ứng dụng', 'thị giác máy tính', 'AI trên thiết bị biên', 'tên thường gọi: Aaron'],
            interests=[('Thị giác máy tính', 'Nhận dạng, phân vùng và hiểu ảnh, video trong điều kiện thực tế.'), ('Dữ liệu và đánh giá', 'Xây dựng, kiểm chứng dữ liệu và quy trình đánh giá mô hình.'), ('AI trên thiết bị biên', 'Đưa mô hình về chạy trên thiết bị ngoài hiện trường.')], h_int='hướng quan tâm', featured='đề tài tiêu biểu',
            bio='Tôi nghiên cứu trí tuệ nhân tạo ứng dụng, trọng tâm là thị giác máy tính, với mong muốn đưa kết quả nghiên cứu vào các bài toán thực tế tại Việt Nam.',
            go_journey='Xem hành trình', believe='quan điểm nghiên cứu', now='đang thực hiện', t_title='Hành trình nghiên cứu', t_btn='Xem hành trình', t_n='giai đoạn', bump='khó khăn và bài học', hint='cuộn xuống để đi tiếp ↓', unknown='chưa xác định', p_in='dự án trong chặng này', p_tag='dự án', p_stage='giai đoạn', menu='Mục lục', more='Xem thêm', less='Thu gọn', p_close='Quay lại hành trình', p_page='Mở trang riêng của dự án',
            doing='đang thực hiện', read='Xem đề tài', role='Vai trò', where='Nơi thực hiện', status='Trạng thái', links='Minh chứng', nolinks='Sẽ bổ sung khi kết quả được công bố.',
            back='Tất cả đề tài', cv='Lý lịch khoa học (PDF)', contact='Liên hệ',
            d_journey='Quá trình học tập, nghiên cứu và định hướng sắp tới.', d_work='Các đề tài đã có công bố, bộ dữ liệu hoặc mã nguồn công khai.', d_about='Thế mạnh, hạn chế đang khắc phục, lý lịch khoa học và liên hệ.',
            h_journey='Hành trình nghiên cứu', s_journey='Các giai đoạn học tập và nghiên cứu từ năm 2021 đến nay, cùng định hướng sắp tới.',
            h_work='Nghiên cứu', s_work='Mỗi đề tài đều kèm minh chứng: bài báo, bộ dữ liệu hoặc mã nguồn công khai.',
            h_pubs='Công bố', s_pubs='Thứ tự tác giả ghi theo nhà xuất bản hoặc kho lưu trữ. Chấm xanh đánh dấu công bố trọng điểm.',
            h_about='Giới thiệu', s_about='Tôi làm nghiên cứu ứng dụng về trí tuệ nhân tạo và định hướng theo con đường nghiên cứu, giảng dạy đại học.'),
 'en': dict(home='Home', journey='Journey', work='Research', pubs='Publications', about='About', notes='Notes',
            slogan='Technology only matters when it <em>reaches people.</em>', slogan_plain='Technology only matters when it reaches people.',
            who='I am <b>Nguyen Ngoc Gia Ninh</b>, known as Aaron, an AI researcher at GREEN-X, VinUniversity. I build datasets and computer vision systems for problems close to people: first patients, now the sea.',
            hello='Hello, I am', name='Nguyen Ngoc<br>Gia Ninh', myrole='Research Assistant · GREEN-X, VinUniversity', words=['applied artificial intelligence', 'computer vision', 'edge AI', 'also known as Aaron'],
            interests=[('Computer vision', 'Recognition, segmentation and understanding of images and video under real-world conditions.'), ('Data and evaluation', 'Building and validating datasets and model evaluation protocols.'), ('Edge AI', 'Running models on devices deployed in the field.')], h_int='research interests', featured='featured project',
            bio='I work on applied artificial intelligence with a focus on computer vision, aiming to bring research results to real-world problems in Vietnam.',
            go_journey='See the journey', believe='research outlook', now='in progress', t_title='Research journey', t_btn='See the journey', t_n='stages', bump='difficulties and lessons', hint='scroll down to continue ↓', unknown='not yet known', p_in='projects in this stage', p_tag='project', p_stage='stage', menu='Menu', more='More', less='Less', p_close='Back to the journey', p_page='Open the project page',
            doing='in progress', read='View project', role='Role', where='Where', status='Status', links='Evidence', nolinks='Links will appear when results are public.',
            back='All projects', cv='Download CV (PDF)', contact='Contact',
            d_journey='Study, research and the plan ahead.', d_work='Projects with a publication, dataset or public code.', d_about='Strengths, current limitations, CV and contact.',
            h_journey='Research journey', s_journey='Stages of study and research since 2021, and the plan ahead.',
            h_work='Research', s_work='Each project is backed by a paper, a dataset or public code.',
            h_pubs='Publications', s_pubs='Author order as listed by the publisher or repository. A green dot marks a featured output.',
            h_about='About', s_about='I work on applied AI and am on my way to becoming a researcher and university lecturer.'),
}
URL = {'vi': dict(home='index.html', journey='hanh-trinh.html', work='cong-viec.html', pubs='cong-bo.html', about='gioi-thieu.html', notes='ghi-chep.html', workdir='cong-viec/'),
       'en': dict(home='en/index.html', journey='en/journey.html', work='en/work.html', pubs='en/publications.html', about='en/about.html', notes='en/notes.html', workdir='en/work/')}

WORK = [
 dict(slug='ntcoral', star=True, title='NTCoral', year='2025–',
  vi=dict(sub='Bộ dữ liệu ảnh rạn san hô Việt Nam, xây dựng từ video khảo sát dưới nước và được chuyên gia sinh học biển kiểm chứng.',
          role='Phụ trách dữ liệu; tác giả thứ nhất của bài báo đang chuẩn bị', where='GREEN-X, VinUniversity', status='Đang thực hiện',
          body=[('Đặt vấn đề', ['Phần lớn bộ dữ liệu san hô công khai được thu ở các vùng biển khác. Ảnh rạn san hô Việt Nam có nhãn còn rất ít, nên chưa thể đánh giá các mô hình hiện có hoạt động ra sao trên dữ liệu trong nước và cần bổ sung bao nhiêu nhãn.'], []),
                ('Phần việc đảm nhận', [], ['Phụ trách quy trình từ video khảo sát đến ảnh phát hành: rà soát video, chọn khung hình, kiểm tra chất lượng và bàn giao gán nhãn.', 'Phối hợp với chuyên gia sinh học biển gán nhãn đến cấp chi.', 'Thiết kế phương pháp chọn khung hình: loại ảnh trùng lặp, sàng lọc chất lượng, bảo đảm độ phủ giữa các điểm khảo sát.', 'Đánh giá mô hình phân vùng ảnh với ít mẫu (few-shot) trên dữ liệu trong nước.']),
                ('Quy trình', [], ['Video khảo sát', 'Chọn khung hình', 'Kiểm tra chất lượng', 'Mô hình đề xuất nhãn', 'Chuyên gia kiểm chứng', 'Bộ dữ liệu mở'])]),
  en=dict(sub='An expert-verified image dataset of Vietnamese coral reefs, built from underwater video surveys.',
          role='Data lead; first author of the paper in preparation', where='GREEN-X, VinUniversity', status='In progress',
          body=[('Why it matters', ['Public coral datasets come mostly from other regions. Vietnamese reefs have very few labelled images, so nobody yet knows how far existing models transfer or how many local labels are needed.'], []),
                ('What I do', [], ['Lead the pipeline from survey video to released images: video review, frame selection, quality checks, annotation hand-off.', 'Coordinate genus-level annotation with marine biologists.', 'Design frame selection: remove near-duplicates, screen quality, keep coverage across survey sites.', 'Evaluate few-shot segmentation models on local data.']),
                ('Pipeline', [], ['Survey video', 'Frame selection', 'Quality loop', 'Model proposals', 'Expert verification', 'Open dataset'])]),
  links=[]),
 dict(slug='vlr', star=False, title_vi='Nhận dạng tiếng nói qua khẩu hình tiếng Việt', title_en='Vietnamese lip reading', year='2024–2026',
  vi=dict(sub='Bộ dữ liệu đọc khẩu hình tiếng Việt quy mô lớn, hướng tới hỗ trợ người gặp khó khăn về phát âm và thính giác.',
          role='Xây dựng quy trình dữ liệu và thực nghiệm cơ sở; khóa luận tốt nghiệp', where='Perception Technology Solutions, Đại học FPT', status='Dữ liệu đã công bố; bài báo ở dạng tiền ấn phẩm',
          body=[('Đặt vấn đề', ['Đọc khẩu hình là bài toán nhận dạng lời nói chỉ từ chuyển động môi. Kỹ thuật này có thể hỗ trợ người mất khả năng phát âm, nhưng tiếng Việt gần như chưa có dữ liệu công khai.'], []),
                ('Phần việc đảm nhận', [], ['Thu thập và tiền xử lý video: phân đoạn, căn chỉnh, trích vùng miệng.', 'Huấn luyện và đánh giá các mô hình cơ sở VSP-LLM và Auto-AVSR.', 'Thử nghiệm mô hình gọn nhẹ trên NVIDIA Jetson Nano.'])]),
  en=dict(sub='A large-scale Vietnamese lip-reading dataset, aimed at people with speech or hearing difficulties.',
          role='Data pipeline and baseline experiments; capstone thesis', where='Perception Technology Solutions, FPT University', status='Dataset public, paper as preprint',
          body=[('Why it matters', ['Lip reading recognises speech from mouth motion alone. It can help people who have lost their voice, but Vietnamese had almost no public data.'], []),
                ('What I did', [], ['Sourced and pre-processed video: segmentation, alignment, mouth-region extraction.', 'Trained and evaluated VSP-LLM and Auto-AVSR baselines.', 'Ran lightweight models on an NVIDIA Jetson Nano.'])]),
  links=[('Zenodo', 'https://doi.org/10.5281/zenodo.19709456'), ('Preprint', 'https://doi.org/10.22541/au.177368999.91959735/v1')]),
 dict(slug='aquaculture', star=False, title_vi='Ra quyết định tự động trong nuôi trồng thuỷ sản thông minh', title_en='Autonomous decision-making in smart aquaculture', year='2026',
  vi=dict(sub='Bài tổng quan về chuỗi từ giám sát đến tác động trong nuôi trồng thuỷ sản.', role='Tác giả Mục 6: Ra quyết định tự động và điều khiển vòng kín', where='Hợp tác nhiều đơn vị', status='Tiền ấn phẩm; đang bình duyệt',
          body=[('Nội dung', ['Bài tổng quan liên kết bốn khâu của nuôi trồng thuỷ sản thông minh: thu nhận dữ liệu, phân tích bằng AI, ra quyết định và cơ cấu chấp hành. Tôi viết phần ra quyết định tự động và điều khiển vòng kín.'], [])]),
  en=dict(sub='A system-level survey: from monitoring to action.', role='Author of Section 6, Autonomous Decision-Making and Closed-Loop Control', where='Multi-institution collaboration', status='Preprint, under review',
          body=[('Overview', ['The survey connects four stages of smart aquaculture: sensing, AI-based understanding, decision-making and actuation. I wrote the section on autonomous decision-making and closed-loop control.'], [])]),
  links=[('Preprint', 'https://doi.org/10.13140/RG.2.2.24130.95688')]),
 dict(slug='aneurysm', star=False, title_vi='Phát hiện phình động mạch nội sọ', title_en='Intracranial aneurysm detection', year='2026',
  vi=dict(sub='Phương pháp học sâu nhiều giai đoạn; công bố dưới dạng chương sách.', role='Đồng tác giả', where='CRC Press, Intelligent Precision Healthcare', status='Đã xuất bản 2026',
          body=[('Nội dung', ['Chương sách trong tuyển tập Intelligent Precision Healthcare (CRC Press, 2026), trang 287–301.'], [])]),
  en=dict(sub='A multistage deep learning approach, published as a book chapter.', role='Co-author', where='CRC Press, Intelligent Precision Healthcare', status='Published 2026',
          body=[('Overview', ['A chapter in the edited volume Intelligent Precision Healthcare (CRC Press, 2026), pages 287–301.'], [])]),
  links=[('DOI', 'https://doi.org/10.1201/9781003667360-21')]),
]

PUBS = [  # (năm, star, tiêu đề, tác giả, nơi_vi, nơi_en, link)
 ('2026', True, 'NTCoral: an expert-annotated image dataset of Vietnamese coral reefs (working title)', f'{ME}, et al.', 'Bài báo dữ liệu đang chuẩn bị, tác giả thứ nhất', 'Dataset paper in preparation, first author', None),
 ('2026', False, 'A Multistage Deep Learning Approach for Intracranial Aneurysm Detection', f'N. P. T. Thao, {ME}, T. N. Quoc, V. T. Hoang', 'Chương sách, Intelligent Precision Healthcare, CRC Press, tr. 287–301', 'Book chapter, Intelligent Precision Healthcare, CRC Press, pp. 287–301', 'https://doi.org/10.1201/9781003667360-21'),
 ('2026', False, 'From Monitoring to Action: A Comprehensive Survey of Autonomous Decision-Making in Smart Aquaculture Systems', f'Q.-H. N. Dam, P. H. Nguyen, M. P. Tran, C.-S. Trinh, T. T. Nguyen, {ME}, et al.', 'Tiền ấn phẩm; đang bình duyệt tại Computers and Electronics in Agriculture', 'Preprint; under review at Computers and Electronics in Agriculture', 'https://doi.org/10.13140/RG.2.2.24130.95688'),
 ('2026', False, 'A Large-Scale Vietnamese Lip Reading Dataset and Enhanced Recognition Pipeline', f'T. N. Quoc, N. P. T. Thao, {ME}, et al.', 'Tiền ấn phẩm', 'Preprint', 'https://doi.org/10.22541/au.177368999.91959735/v1'),
 ('2026', False, 'A Large-Scale Vietnamese Lip-Reading Dataset for Visual Speech Recognition', f'T. N. Quoc, N. P. T. Thao, {ME}, H. D. N. Quynh, V. T. Hoang, et al.', 'Bộ dữ liệu, Zenodo, v3, CC BY 4.0', 'Dataset, Zenodo, v3, CC BY 4.0', 'https://doi.org/10.5281/zenodo.19709456'),
]

JOURNEY = [  # GIAI ĐOẠN: (thời gian, vi(tiêu đề, đoạn, [khó khăn và bài học]), en(...), next?, công trình chính: school|tower|vinuni|goal)
 ('2021–2025', ('Trường Đại học FPT', 'Cử nhân Công nghệ thông tin, chuyên ngành Trí tuệ nhân tạo. Đồ án tốt nghiệp: nhận dạng tiếng nói qua khẩu hình cho tiếng Việt.', 'Khó khăn lớn nhất của đồ án không nằm ở mô hình mà ở dữ liệu: tiếng Việt gần như chưa có bộ dữ liệu công khai cho bài toán đọc khẩu hình, nên nhóm phải tự xây dựng từ đầu.'),
               ('FPT University', 'Bachelor in Information Technology, Artificial Intelligence specialisation. Capstone project: visual speech recognition for Vietnamese.', 'The main difficulty of the capstone was data rather than models: Vietnamese had almost no public lip-reading dataset, so the team had to build one from scratch.'), False, 'school'),
 ('2025–2026', ('VinBigData', 'Chương trình đào tạo chuyên sâu về thị giác máy tính, xử lý ngôn ngữ tự nhiên, AI tạo sinh và MLOps. Tại đây tham gia đề tài phát hiện phình động mạch nội sọ bằng học sâu.'),
               ('VinBigData', 'An intensive programme in computer vision, natural language processing, generative AI and MLOps, including a project on deep-learning detection of intracranial aneurysms.'), False, 'tower'),
 ('2026–', ('GREEN-X, VinUniversity', 'Trợ lý nghiên cứu. Phụ trách xây dựng NTCoral, bộ dữ liệu ảnh rạn san hô Việt Nam, phối hợp với các nhà sinh học biển.', 'Điều kiện thực địa khắc nghiệt hơn phòng thí nghiệm: thiết bị đặt ngoài biển không phải lúc nào cũng vận hành ổn định, và mỗi lần hỏng hóc buộc nhóm phải xem lại thiết kế.'),
           ('GREEN-X, VinUniversity', 'Research Assistant, responsible for building NTCoral, a Vietnamese coral reef image dataset, together with marine biologists.', 'Field conditions are harsher than the lab: equipment deployed at sea does not always run reliably, and each failure sends the team back to the design.'), False, 'vinuni'),
 ('', ('Định hướng', 'Học tiếp thạc sĩ và tiến sĩ ở nước ngoài, sau đó trở về giảng dạy đại học tại Việt Nam. Hướng chuyên sâu dự kiến là AI trên thiết bị biên (edge AI) phục vụ quan trắc ngoài hiện trường. Chặng đường này còn dài và còn nhiều điều chưa xác định.'),
       ('Outlook', 'A master’s degree and a PhD abroad, then a return to Vietnam to teach at a university. The intended specialisation is edge AI for field monitoring. This stretch is long, and much of it is still unknown.'), True, 'goal'),
]

ABOUT = {
 'vi': [('Thế mạnh', ['Tư duy tổ chức: hệ thống hoá dữ liệu và quy trình thành các bước có thể truy vết và kiểm chứng, phù hợp với công việc xây dựng bộ dữ liệu.', 'Phối hợp liên ngành: đã làm việc cùng các nhà sinh học biển, kỹ sư điện tử và kỹ sư tự động hoá.']),
        ('Hạn chế đang khắc phục', ['Chiều sâu chuyên môn. Tôi tiếp cận trí tuệ nhân tạo từ phía ứng dụng, nên nền tảng lý thuyết và hệ thống nhúng là những phần cần bổ sung. Đây cũng là lý do tôi dự định học tiếp sau đại học.']),
        ('Hiện tại và định hướng', ['Hiện là trợ lý nghiên cứu, đã có những công bố đầu tiên và một bộ dữ liệu mở. Dự định tiếp theo là học thạc sĩ, tiến sĩ, rồi giảng dạy đại học. Chi tiết ở trang Hành trình.'])],
 'en': [('Strengths', ['Organising. I am good at turning messy data and processes into ordered, traceable systems, which is why dataset building suits me.', 'Working well across disciplines: marine biologists, electronics engineers, automation engineers. I believe everyone has something to teach.']),
        ('What I am building up', ['Technical depth. I came to AI through applications, so theory and embedded systems are what I need to learn next. This is also why I am going to graduate school.']),
        ('Where I am, where I am going', ['Currently a research assistant with first publications and one open dataset. Next: a master’s, a PhD, then teaching. See the Journey page.'])],
}
NOTES = []  # thêm bài viết ngắn ở đây; có bài thì mục Ghi chép tự hiện

def rel(frm, to):
    return os.path.relpath(to, os.path.dirname(frm) or '.')
def title_of(w, lang): return w.get('title') or w[f'title_{lang}']

# DỰ ÁN nằm trong giai đoạn nào (chỉ số trong JOURNEY, bắt đầu từ 0) và gắn vào vật thể 3D nào:
#   (slug trong WORK, vật thể: kiosk = phòng thu khẩu hình | hospital = bệnh viện | buoy = trạm phao ngoài biển, tên ngắn vi, tên ngắn en)
STAGE_PROJECTS = {
    0: [('vlr', 'kiosk', 'Đọc khẩu hình tiếng Việt', 'Vietnamese lip reading')],
    1: [('aneurysm', 'hospital', 'Phát hiện phình động mạch nội sọ', 'Intracranial aneurysm detection')],
    2: [('ntcoral', 'buoy', 'NTCoral', 'NTCoral')],
}
# CỘT MỐC: việc có thật nhưng không phải dự án và không phải giai đoạn (vật thể nhỏ, nhãn nhỏ, không bấm được)
#   (vật thể: cert = chứng chỉ | teky = lớp học nhỏ, nhãn vi, nhãn en)
MILESTONES = {
    0: [('cert', 'Chứng chỉ nghiệp vụ sư phạm · 2025', 'Pedagogy certificate · 2025'), ('teky', 'Trợ giảng lập trình · TEKY', 'Programming teaching assistant · TEKY')],
}
# Trở ngại trên đường ứng với "khó khăn và bài học" của giai đoạn: holes = ổ gà | flood = ngập nước, cát tràn | rocks = đá lở
OBSTACLE = {0: 'holes', 2: 'flood'}

def stage_json(lang):
    out = []
    for i, (when, vi, en, nx, icon) in enumerate(JOURNEY):
        d = vi if lang == 'vi' else en
        pj = [dict(slug=s, anchor=a, title=E(tv if lang == 'vi' else te)) for s, a, tv, te in STAGE_PROJECTS.get(i, [])]
        ms = [dict(kind=k, label=E(lv if lang == 'vi' else le)) for k, lv, le in MILESTONES.get(i, [])]
        out.append(dict(when=when, title=d[0], paras=[E(d[1])], lesson=E(d[2]) if len(d) > 2 else '', icon=icon, projects=pj, milestones=ms, obstacle=OBSTACLE.get(i, 'holes')))
    return E(json.dumps(out, ensure_ascii=False))

def proj_parts(w, lang):
    parts = ''
    for h, paras, items in w[lang]['body']:
        tag = 'ol' if h in ('Quy trình', 'Pipeline') else 'ul'
        parts += f'<h2>{E(h)}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in paras) + (f'<{tag}>' + ''.join(f'<li>{E(x)}</li>' for x in items) + f'</{tag}>' if items else '')
    lk = ''.join(f'<div><a class="link" href="{u}">{E(n)}</a></div>' for n, u in w['links']) or f'<div>{T[lang]["nolinks"]}</div>'
    return parts, lk

def proj_template(w, lang, p):
    t = T[lang]; d = w[lang]; parts, lk = proj_parts(w, lang)
    return f'''<template id="proj-{w['slug']}"><header class="phead"><div class="mono">{t['p_tag']} · {w['year']}</div><h2>{E(title_of(w, lang))}</h2><p>{E(d['sub'])}</p></header>
<dl class="pmeta"><div><dt>{t['role']}</dt><dd>{E(d['role'])}</dd></div><div><dt>{t['where']}</dt><dd>{E(d['where'])}</dd></div><div><dt>{t['status']}</dt><dd>{E(d['status'])}</dd></div></dl>
<div class="prose">{parts}</div><div class="plinks"><h4>{t['links']}</h4>{lk}<a class="btn" href="{rel(p, U['workdir'] + w['slug'] + '.html')}">{t['p_page']}</a></div></template>'''

def shell(lang, key, path, title, body, extra=''):
    t = T[lang]; other = 'en' if lang == 'vi' else 'vi'
    # trang tương ứng ở ngôn ngữ kia
    if path.startswith(URL[lang]['workdir']): twin = URL[other]['workdir'] + os.path.basename(path)
    else: twin = URL[other][key]
    items = ['journey', 'work', 'pubs', 'about'] + (['notes'] if NOTES else [])
    nav = ''.join(f'<a class="item{" on" if k == key else ""}" href="{rel(path, URL[lang][k])}">{t[k]}</a>' for k in items)
    a = lambda p: rel(path, p)
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(t['slogan_plain'])} Aaron (Nguyen Ngoc Gia Ninh), GREEN-X, VinUniversity.">
<link rel="icon" href="{a('assets/clover.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Be+Vietnam+Pro:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a('assets/style.css')}"></head><body>
<header class="nav"><a class="brand" href="{a(URL[lang]['home'])}"><img src="{a('assets/clover.svg')}" alt="">Aaron</a><nav class="links" id="navlinks">{nav}<a class="lang" href="{a(twin)}" hreflang="{other}">{other.upper()}</a></nav><button type="button" class="burger" aria-label="{t['menu']}" aria-expanded="false" aria-controls="navlinks"><i></i><i></i><i></i></button></header>
<main>{body}</main>
<footer class="foot"><div class="wrap"><span class="q">{E(t['slogan_plain'])}</span><a class="link" href="mailto:{EMAIL}">{EMAIL}</a><a class="link" href="https://github.com/Zhaninh">GitHub</a><a class="link" href="https://www.linkedin.com/in/gianinh-948586299/">LinkedIn</a></div></footer>
<script src="{a('assets/main.js')}"></script>{extra}</body></html>'''

def write(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full), exist_ok=True); open(full, 'w').write(s)

def head(t1, p, label=''):
    return f'<section class="page-head"><div class="wrap">{f"<div class=mono>{E(label)}</div>" if label else ""}<h1>{E(t1)}</h1><p>{E(p)}</p></div></section>'

for lang in ('vi', 'en'):
    t = T[lang]; U = URL[lang]
    # ---- trang chủ ----
    p = U['home']; f = next(w for w in WORK if w['star']); fw = f[lang]
    doors = ''.join(f'<a class="row reveal" href="{rel(p, U[k])}"><h3>{t[k]}</h3><p>{E(t["d_" + k])}</p><span class="mono">{n}</span></a>'
                    for k, n in (('journey', f'{len(JOURNEY)}'), ('work', f'{len(WORK)}'), ('about', 'CV')))
    ints = ''.join(f'<li><b>{E(a)}</b><span>{E(d)}</span></li>' for a, d in t['interests'])
    three = f'<script src="{rel(p, "assets/three.min.js")}"></script><script src="{rel(p, "assets/journey3d.js")}"></script>'
    body = f'''<section class="hero"><div class="wrap hero-grid"><div>
<div class="hello">{t['hello']}</div>
<h1 class="name">{t['name']}</h1>
<p class="role">{t['myrole']}</p><div class="typed" data-words="{E(json.dumps(t['words'], ensure_ascii=False))}"></div>
<p class="bio">{t['bio']}</p>
<div class="acts"><a class="btn pri" href="{rel(p, U['journey'])}">{t['go_journey']}</a><a class="btn" href="{rel(p, 'assets/Aaron_CV.pdf')}">CV</a><a class="btn" href="https://github.com/Zhaninh">GitHub</a><a class="btn" href="https://www.linkedin.com/in/gianinh-948586299/">LinkedIn</a></div></div>
<div class="portrait reveal"><div class="disc"></div><div class="orbit"><i></i></div><img class="me" src="{rel(p, 'assets/aaron_cut.webp')}" alt="{E(t['name'].replace('<br>', ' '))}" width="760" height="1000"></div></div></section>
<section class="belief"><div class="wrap belief-grid"><div class="reveal"><div class="mono">{t['believe']}</div><q>{t['slogan']}</q></div>
<div class="reveal"><div class="mono">{t['h_int']}</div><ol class="ints">{ints}</ol></div></div></section>
<section class="teaser-wrap"><div class="wrap"><a class="teaser reveal" href="{rel(p, U['journey'])}" data-j3d="teaser" data-stages="{stage_json(lang)}"><canvas></canvas><div class="cap"><div class="mono">{len(JOURNEY)} {t['t_n']}</div><h2>{t['t_title']}</h2><p>{E(t['d_journey'])}</p><span class="btn pri">{t['t_btn']}</span></div></a></div></section>
<section><div class="wrap"><a class="feature spot reveal" href="{rel(p, U['workdir'] + f['slug'] + '.html')}"><div><div class="mono">{t['featured']}</div><h2>{E(title_of(f, lang))}</h2><p>{E(fw['sub'])}</p></div><span class="go">{t['read']}</span></a></div></section>
<section><div class="wrap"><div class="rows">{doors}</div></div></section>'''
    write(p, shell(lang, 'home', p, ('Nguyễn Ngọc Gia Ninh (Aaron)' if lang == 'vi' else 'Nguyen Ngoc Gia Ninh (Aaron)') + ' · ' + t['myrole'], body, three))
    # ---- hành trình ----
    p = U['journey']
    lis = ''.join(f'<li class="reveal{" next" if nx else ""}"><div class="mono">{E(when)}</div><div><h3>{E((vi if lang == "vi" else en)[0])}</h3>{"".join(f"<p>{E(x)}</p>" for x in (vi if lang == "vi" else en)[1:])}{"".join(f"<p><a class=link href={rel(p, U['workdir'] + s + '.html')}>{E(tv if lang == 'vi' else te)}</a></p>" for s, a, tv, te in STAGE_PROJECTS.get(i, []))}</div></li>' for i, (when, vi, en, nx, _) in enumerate(JOURNEY))
    wmap = {w['slug']: w for w in WORK}
    tpls = ''.join(proj_template(wmap[s], lang, p) for i in sorted(STAGE_PROJECTS) for s, a, tv, te in STAGE_PROJECTS[i])
    j3d = f'''<section class="j3d" data-j3d="full" style="--n:9" data-stage="{t['p_stage']}" data-more="{t['more']}" data-less="{t['less']}" data-bump="{t['bump']}" data-unknown="{t['unknown']}" data-pin="{t['p_in']}" data-tag="{t['p_tag']}" data-stages="{stage_json(lang)}"><div class="j3d-sticky"><canvas></canvas><div class="j3d-labels"></div>
<article class="j3d-card"><div class="k"></div><h3></h3><div class="tx"></div></article><div class="j3d-hint">{t['hint']}</div></div>
<div class="j3d-panel" aria-hidden="true"><div class="pbar"><button type="button" class="pback">← {t['p_close']}</button><span class="mono pk"></span></div><div class="pbody"></div></div>{tpls}</section>'''
    three = f'<script src="{rel(p, "assets/three.min.js")}"></script><script src="{rel(p, "assets/journey3d.js")}"></script>'
    write(p, shell(lang, 'journey', p, t['journey'] + ' · Aaron', head(t['h_journey'], t['s_journey']) + j3d + f'<section class="path-fallback"><div class="wrap"><ol class="path">{lis}</ol></div></section>', three))
    # ---- công việc ----
    p = U['work']
    rows = ''.join(f'<a class="row reveal{" star" if w["star"] else ""}" href="{rel(p, U["workdir"] + w["slug"] + ".html")}"><h3>{E(title_of(w, lang))}</h3><p>{E(w[lang]["sub"])}</p><span class="mono">{w["year"]}</span></a>' for w in WORK)
    write(p, shell(lang, 'work', p, t['work'] + ' · Aaron', head(t['h_work'], t['s_work']) + f'<section><div class="wrap"><div class="rows">{rows}</div></div></section>'))
    for w in WORK:
        d = w[lang]; p = U['workdir'] + w['slug'] + '.html'
        parts, lk = proj_parts(w, lang)
        body = head(title_of(w, lang), d['sub'], w['year']) + f'''<section><div class="wrap split"><div class="prose reveal">{parts}<p style="margin-top:48px"><a class="link" href="{rel(p, U['work'])}">{t['back']}</a></p></div>
<aside class="box"><h4>{t['role']}</h4><div>{E(d['role'])}</div><h4>{t['where']}</h4><div>{E(d['where'])}</div><h4>{t['status']}</h4><div>{E(d['status'])}</div><h4>{t['links']}</h4>{lk}</aside></div></section>'''
        write(p, shell(lang, 'work', p, title_of(w, lang) + ' · Aaron', body))
    # ---- công bố ----
    p = U['pubs']
    lis = ''.join(f'<li class="reveal{" star" if st else ""}"><span class="mono">{y}</span><div><div class="t">{E(ti)}</div><div class="a">{au}</div><div class="v">{E(vv if lang == "vi" else ve)}</div>{f"<a class=link href={u}>DOI</a>" if u else ""}</div></li>' for y, st, ti, au, vv, ve, u in PUBS)
    write(p, shell(lang, 'pubs', p, t['pubs'] + ' · Aaron', head(t['h_pubs'], t['s_pubs']) + f'<section><div class="wrap"><ol class="pubs">{lis}</ol></div></section>'))
    # ---- giới thiệu ----
    p = U['about']
    parts = ''.join(f'<h2>{E(h)}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in ps) for h, ps in ABOUT[lang])
    body = head(t['h_about'], t['s_about']) + f'''<section><div class="wrap split"><div class="prose reveal">{parts}</div>
<aside class="box"><h4>CV</h4><div><a class="link" href="{rel(p, 'assets/Aaron_CV.pdf')}">{t['cv']}</a></div><h4>{t['contact']}</h4><div><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></div></aside></div></section>'''
    write(p, shell(lang, 'about', p, t['about'] + ' · Aaron', body))

open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
open(os.path.join(ROOT, 'README.md'), 'w').write('# zhaninh.github.io\n\nTrang cá nhân của Nguyễn Ngọc Gia Ninh (Aaron). Sửa nội dung trong `build.py`, chạy `python3 build.py`.\nQuy tắc thiết kế nằm ở đầu `assets/style.css`. Icon cỏ bốn lá: Noto Emoji (Apache 2.0). Bản đồ 3D: three.js r160 (MIT), mã ở `assets/journey3d.js`.\n')
print('ok')
