import re
#!/usr/bin/env python3
"""Trang cá nhân Aaron. Tĩnh, song ngữ (vi mặc định ở gốc, en trong /en/).
Thêm nội dung: thêm một mục vào WORK / PUBS / JOURNEY / NOTES rồi chạy `python3 build.py`.
Mục có "star": True sẽ tự nổi lên (trang chủ lấy mục WORK có star đầu tiên)."""
import os, html, json, time
VER = time.strftime('%Y%m%d%H%M')  # gắn vào link CSS/JS để trình duyệt không dùng bản cũ trong bộ nhớ đệm
ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape
EMAIL = 'aaron89.workplace@gmail.com'  # email cá nhân
EMAIL_WORK = 'ninh.nng@vinuni.edu.vn'
SCHOLAR = 'https://scholar.google.com/citations?user=g0kINu8AAAAJ&hl=vi'
LINKEDIN = 'https://www.linkedin.com/in/gianinh-948586299/'
GREENX = 'https://greenx.vinuni.edu.vn'
ME = '<b class="me">N. N. G. Ninh</b>'

T = {  # chuỗi giao diện
 'vi': dict(home='Trang chủ', journey='Hành trình', work='Dự án', pubs='Công bố', hl='Dấu ấn', about='Giới thiệu', notes='Ghi chép',
            slogan='Công nghệ thật sự có ý nghĩa khi <em>đến được với con người.</em>', slogan_plain='Công nghệ thật sự có ý nghĩa khi đến được với con người.',
            who='Tôi là <b>Nguyễn Ngọc Gia Ninh</b>, thường gọi là Aaron, nghiên cứu viên AI tại GREEN-X, VinUniversity. Tôi xây dữ liệu và hệ thống thị giác máy tính cho những bài toán gần với con người: trước là người bệnh, nay là biển.',
            hello='Xin chào, tôi là', name='Nguyễn Ngọc<br>Gia Ninh', myrole='Trợ lý nghiên cứu · GREEN-X, VinUniversity', role_pre='Trợ lý nghiên cứu tại', mail_work='Công việc', mail_me='Cá nhân', words=['trí tuệ nhân tạo ứng dụng', 'thị giác máy tính', 'AI trên thiết bị biên', 'tên thường gọi: Aaron'],
            interests=[('Thị giác máy tính', 'Nhận dạng, phân vùng và hiểu ảnh, video trong điều kiện thực tế.'), ('Dữ liệu và đánh giá', 'Xây dựng, kiểm chứng dữ liệu và quy trình đánh giá mô hình.'), ('AI trên thiết bị biên', 'Đưa mô hình về chạy trên thiết bị ngoài hiện trường.')], h_int='hướng quan tâm', featured='đề tài tiêu biểu',
            bio='Tôi nghiên cứu trí tuệ nhân tạo ứng dụng, trọng tâm là thị giác máy tính, với mong muốn đưa kết quả nghiên cứu vào các bài toán thực tế tại Việt Nam.',
            go_journey='Đi cùng tôi qua hành trình', j_sub='Bản đồ 3D: các giai đoạn, dự án và chặng phía trước', c_label='liên hệ', believe='quan điểm nghiên cứu', now='đang thực hiện', t_title='Hành trình nghiên cứu', t_btn='Xem hành trình', t_n='giai đoạn', bump='khó khăn và bài học', hint='cuộn xuống để đi tiếp ↓', unknown='chưa xác định', p_in='dự án trong chặng này', p_tag='dự án', p_stage='giai đoạn', menu='Mục lục', more='Xem thêm', less='Thu gọn', p_close='Quay lại hành trình', p_page='Mở trang riêng của dự án',
            doing='đang thực hiện', read='Xem đề tài', role='Vai trò', where='Nơi thực hiện', status='Trạng thái', links='Minh chứng', nolinks='Sẽ bổ sung khi kết quả được công bố.',
            back='Tất cả đề tài', cv='Lý lịch khoa học (PDF)', contact='Liên hệ',
            d_journey='Quá trình học tập, nghiên cứu và định hướng sắp tới.', d_work='Các đề tài đã có công bố, bộ dữ liệu hoặc mã nguồn công khai.', d_about='Thế mạnh, hạn chế đang khắc phục, lý lịch khoa học và liên hệ.',
            h_journey='Hành trình nghiên cứu', s_journey='Các giai đoạn học tập và nghiên cứu từ năm 2021 đến nay, cùng định hướng sắp tới.',
            h_work='Dự án', s_work='Toàn bộ dự án tôi đã và đang làm. Mỗi dự án có trang riêng, và có thể xem nó nằm ở đâu trên hành trình.',
            h_hl='Dấu ấn', s_hl='Những chuyến công tác, sự kiện và khoảnh khắc trên đường đi. Mỗi tấm ảnh đi kèm câu chuyện của nó.', h_pubs='Công bố', s_pubs='Thứ tự tác giả ghi theo nhà xuất bản hoặc kho lưu trữ. Chấm xanh đánh dấu công bố trọng điểm.',
            h_about='Giới thiệu', s_about='Tôi làm nghiên cứu ứng dụng về trí tuệ nhân tạo và định hướng theo con đường nghiên cứu, giảng dạy đại học.'),
 'en': dict(home='Home', journey='Journey', work='Projects', pubs='Publications', hl='Highlights', about='About', notes='Notes',
            slogan='Technology is truly meaningful when it <em>reaches people.</em>', slogan_plain='Technology is truly meaningful when it reaches people.',
            who='I am <b>Nguyen Ngoc Gia Ninh</b>, known as Aaron, an AI researcher at GREEN-X, VinUniversity. I build datasets and computer vision systems for problems close to people: first patients, now the sea.',
            hello='Hello, I am', name='Nguyen Ngoc<br>Gia Ninh', myrole='Research Assistant · GREEN-X, VinUniversity', role_pre='Research Assistant at', mail_work='Work', mail_me='Personal', words=['applied artificial intelligence', 'computer vision', 'edge AI', 'also known as Aaron'],
            interests=[('Computer vision', 'Recognition, segmentation and understanding of images and video under real-world conditions.'), ('Data and evaluation', 'Building and validating datasets and model evaluation protocols.'), ('Edge AI', 'Running models on devices deployed in the field.')], h_int='research interests', featured='featured project',
            bio='I work on applied artificial intelligence with a focus on computer vision, aiming to bring research results to real-world problems in Vietnam.',
            go_journey='Take the journey with me', j_sub='A 3D map of stages, projects and the road ahead', c_label='contact', believe='research outlook', now='in progress', t_title='Research journey', t_btn='See the journey', t_n='stages', bump='difficulties and lessons', hint='scroll down to continue ↓', unknown='not yet known', p_in='projects in this stage', p_tag='project', p_stage='stage', menu='Menu', more='More', less='Less', p_close='Back to the journey', p_page='Open the project page',
            doing='in progress', read='View project', role='Role', where='Where', status='Status', links='Evidence', nolinks='Links will appear when results are public.',
            back='All projects', cv='Download CV (PDF)', contact='Contact',
            d_journey='Study, research and the plan ahead.', d_work='Projects with a publication, dataset or public code.', d_about='Strengths, current limitations, CV and contact.',
            h_journey='Research journey', s_journey='Stages of study and research since 2021, and the plan ahead.',
            h_work='Projects', s_work='Every project I have worked on. Each has its own page, and you can see where it sits on the journey.',
            h_hl='Highlights', s_hl='Field trips, events and moments along the way. Every photo comes with its story.', h_pubs='Publications', s_pubs='Author order as listed by the publisher or repository. A green dot marks a featured output.',
            h_about='About', s_about='I work on applied AI and am on my way to becoming a researcher and university lecturer.'),
}
URL = {'en': dict(home='index.html', journey='journey.html', work='work.html', pubs='publications.html', hl='highlights.html', about='about.html', notes='notes.html', workdir='work/'),  # tiếng Anh là mặc định (ở gốc)
       'vi': dict(home='vi/index.html', journey='vi/hanh-trinh.html', work='vi/cong-viec.html', pubs='vi/cong-bo.html', hl='vi/dau-an.html', about='vi/gioi-thieu.html', notes='vi/ghi-chep.html', workdir='vi/cong-viec/')}

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

PUBS = [  # (năm, star, tiêu đề, tác giả, nơi_vi, nơi_en, link, dự án)
 ('2026', True, 'NTCoral: an expert-annotated image dataset of Vietnamese coral reefs (working title)', f'{ME}, et al.', 'Bài báo dữ liệu đang chuẩn bị, tác giả thứ nhất', 'Dataset paper in preparation, first author', None, 'ntcoral'),
 ('2026', False, 'A Multistage Deep Learning Approach for Intracranial Aneurysm Detection', f'N. P. T. Thao, {ME}, T. N. Quoc, V. T. Hoang', 'Chương sách, Intelligent Precision Healthcare, CRC Press, tr. 287–301', 'Book chapter, Intelligent Precision Healthcare, CRC Press, pp. 287–301', 'https://doi.org/10.1201/9781003667360-21', 'aneurysm'),
 ('2026', False, 'From Monitoring to Action: A Comprehensive Survey of Autonomous Decision-Making in Smart Aquaculture Systems', f'Q.-H. N. Dam, P. H. Nguyen, M. P. Tran, C.-S. Trinh, T. T. Nguyen, {ME}, et al.', 'Tiền ấn phẩm; đang bình duyệt tại Computers and Electronics in Agriculture', 'Preprint; under review at Computers and Electronics in Agriculture', 'https://doi.org/10.13140/RG.2.2.24130.95688', 'aquaculture'),
 ('2026', False, 'A Large-Scale Vietnamese Lip Reading Dataset and Enhanced Recognition Pipeline', f'T. N. Quoc, N. P. T. Thao, {ME}, et al.', 'Tiền ấn phẩm', 'Preprint', 'https://doi.org/10.22541/au.177368999.91959735/v1', 'vlr'),
 ('2026', False, 'A Large-Scale Vietnamese Lip-Reading Dataset for Visual Speech Recognition', f'T. N. Quoc, N. P. T. Thao, {ME}, H. D. N. Quynh, V. T. Hoang, et al.', 'Bộ dữ liệu, Zenodo, v3, CC BY 4.0', 'Dataset, Zenodo, v3, CC BY 4.0', 'https://doi.org/10.5281/zenodo.19709456', 'vlr'),
]

FB_TA = 'Phan Thục Anh (Facebook)'; FB_GX = 'GREEN-X (Facebook)'
STORIES = [  # (ngày ISO, ngày hiển thị, nơi_vi, nơi_en, tiêu đề_vi, tiêu đề_en, tóm tắt_vi, tóm tắt_en, [ảnh], [(nhãn, link)], [thẻ])
 ('2026-10-25', '24–26.10.2026', 'Nha Trang, Khánh Hòa', 'Nha Trang, Khanh Hoa',
  'Gian triển lãm GREEN-X tại Ngày hội Chuyển đổi số', 'GREEN-X booth at the Digital Transformation Expo',
  'Lần đầu GREEN-X có gian trưng bày riêng, giới thiệu giải pháp cho đô thị xanh, du lịch bền vững, nuôi biển và bảo tồn biển. Robot đại dương phát triển cùng VinaTech là điểm dừng chân đông khách nhất.',
  'GREEN-X ran its own booth for the first time, showing solutions for green cities, sustainable tourism, mariculture and marine conservation. The ocean robot built with VinaTech drew the biggest crowd.',
  ['expo_0', 'expo_1'], [(FB_GX, 'https://www.facebook.com/share/p/19jbPiY6e9/')], ['GREEN-X', 'Khánh Hòa']),
 ('2026-07-01', '07.2026', 'Nha Trang và Vân Phong, Khánh Hòa', 'Nha Trang and Van Phong, Khanh Hoa',
  'Trở lại Khánh Hòa: du lịch xanh, Hòn Mun và nuôi biển', 'Back in Khanh Hoa: green tourism, Hon Mun and mariculture',
  'Chuyến công tác nối tiếp Cần Giờ: làm việc với Sở Văn hóa, Thể thao và Du lịch về Bộ tiêu chuẩn Du lịch Xanh, chuẩn bị hạ thủy hệ thống IoT quan trắc đa dạng sinh học ở Hòn Mun, và thăm trang trại cá chẽm công nghệ cao của Australis ở Vân Phong để bàn hướng AI cho nuôi biển.',
  'A trip right after Can Gio: meetings with the provincial tourism department on the Green Tourism standard, preparing to deploy the IoT biodiversity-monitoring system at Hon Mun, and a visit to Australis’ high-tech sea-bass farm at Van Phong to discuss AI for mariculture.',
  ['nhatrang_0', 'nhatrang_1'], [(FB_TA, 'https://www.facebook.com/share/p/14zHYMXiH5c/')], ['Công tác', 'IoT']),
 ('2026-06-20', '06.2026', 'Cần Giờ, TP. Hồ Chí Minh', 'Can Gio, Ho Chi Minh City',
  'Khảo sát rừng ngập mặn Cần Giờ', 'Surveying the Can Gio mangroves',
  'Làm việc với Ban Quản lý rừng phòng hộ Cần Giờ và khảo sát thực địa. GREEN-X giới thiệu hệ thống bảo tồn rừng ngập mặn kết hợp viễn thám, IoT, AI và digital twin, với mục tiêu chung là biến Cần Giờ thành một living lab về công nghệ bảo tồn.',
  'Meetings and a field survey with the Can Gio protection-forest board. GREEN-X presented a mangrove conservation system combining remote sensing, IoT, AI and a digital twin, with the shared aim of making Can Gio a living lab for conservation technology.',
  ['cangio_0', 'cangio_1', 'cangio_2'], [(FB_TA, 'https://www.facebook.com/share/p/19k7V5EHyh/')], ['Công tác', 'Thực địa']),
 ('2026-06-10', '06.2026', 'VinUniversity, Hà Nội', 'VinUniversity, Hanoi',
  'VinUni Research Day', 'VinUni Research Day',
  'Gian GREEN-X kể các dự án chính sách qua poster và video, còn phần công nghệ thì cho xem tận mắt: nền tảng quan sát cá theo thời gian thực ở Nha Trang và robot đại dương vừa bơi vừa bay.',
  'The GREEN-X booth told its policy projects through posters and video, and let visitors see the technology directly: a live fish-watching platform from Nha Trang and an ocean robot that both swims and flies.',
  ['researchday_0', 'researchday_3', 'researchday_1'], [(FB_TA, 'https://www.facebook.com/share/p/1KzcXVeNf4/')], ['Sự kiện', 'VinUni']),
 ('2026-03-09', '09.03.2026', 'VinUniversity, Hà Nội', 'VinUniversity, Hanoi',
  'GREEN-X Meet & Greet', 'GREEN-X Meet & Greet',
  'Buổi gặp mặt đầu tiên để giới thiệu trung tâm GREEN-X với cộng đồng VinUni và cảm ơn các phòng ban đã đồng hành.',
  'The first gathering to introduce GREEN-X to the VinUni community and thank the teams that supported the centre.',
  ['meetgreet_0', 'meetgreet_3'], [(FB_GX, 'https://www.facebook.com/share/p/1QRhLrPxH5/')], ['GREEN-X', 'Sự kiện']),
 ('2026-01-20', '01.2026', 'GREEN-X, VinUniversity', 'GREEN-X, VinUniversity',
  'Những ngày đầu ở GREEN-X', 'My first weeks at GREEN-X',
  'Tôi vào GREEN-X với vai trò trợ lý nghiên cứu ngay trước khi trung tâm nhận văn phòng mới. Những tuần đầu là buổi định hướng cùng các nghiên cứu viên sau tiến sĩ và trợ lý nghiên cứu mới, rồi cả nhóm dọn về không gian làm việc ở tầng 5, toà I. Một khởi đầu cùng lúc với nhiều gương mặt mới.',
  'I joined GREEN-X as a research assistant just before the centre moved into its new office. My first weeks began with an orientation alongside the new postdoctoral researchers and research assistants, and then the whole team moved into the new workspace on level 5 of Building I. A start shared with many new faces.',
  ['orientation_0', 'newhome_0', 'office_0'], [(FB_GX, 'https://www.facebook.com/share/p/18qWXJCYuS/'), (FB_GX, 'https://www.facebook.com/share/p/1E9hu3bkte/'), (FB_TA, 'https://www.facebook.com/share/p/1KAqXcWBeZ/')], ['GREEN-X', 'Cột mốc']),
]
TAG_EN = {'Cột mốc': 'Milestone', 'Công tác': 'Field trip', 'Thực địa': 'Fieldwork', 'Sự kiện': 'Event'}

NEWS = [  # (ngày hiển thị, nội dung_vi, nội dung_en, đích: ('hl', id) | ('work', slug) | None)
 ('10.2026', 'GREEN-X lần đầu có gian trưng bày tại Ngày hội Chuyển đổi số Khánh Hòa 2026.', 'GREEN-X ran its first exhibition booth at Khanh Hoa Digital Transformation Day 2026.', ('hl', 'expo')),
 ('04.2026', 'Chính thức là trợ lý nghiên cứu tại GREEN-X, VinUniversity, phụ trách dự án NTCoral.', 'Started as a research assistant at GREEN-X, VinUniversity, leading the NTCoral project.', ('work', 'ntcoral')),
 ('2026', 'Chương sách về phát hiện phình động mạch nội sọ được xuất bản trong Intelligent Precision Healthcare (CRC Press).', 'Book chapter on intracranial aneurysm detection published in Intelligent Precision Healthcare (CRC Press).', ('work', 'aneurysm')),
 ('2026', 'Bộ dữ liệu đọc khẩu hình tiếng Việt quy mô lớn được phát hành trên Zenodo.', 'Large-scale Vietnamese lip-reading dataset released on Zenodo.', ('work', 'vlr')),
]

JOURNEY = [  # GIAI ĐOẠN: (thời gian, vi(tiêu đề, đoạn, [khó khăn và bài học]), en(...), next?, công trình chính: school|tower|vinuni|goal)
 ('2021–2025', ('Trường Đại học FPT', 'Cử nhân Công nghệ thông tin, chuyên ngành Trí tuệ nhân tạo. Đồ án tốt nghiệp: nhận dạng tiếng nói qua khẩu hình cho tiếng Việt.', 'Khó khăn lớn nhất của đồ án không nằm ở mô hình mà ở dữ liệu: tiếng Việt gần như chưa có bộ dữ liệu công khai cho bài toán đọc khẩu hình, nên nhóm phải tự xây dựng từ đầu.'),
               ('FPT University', 'Bachelor in Information Technology, Artificial Intelligence specialisation. Capstone project: visual speech recognition for Vietnamese.', 'The main difficulty of the capstone was data rather than models: Vietnamese had almost no public lip-reading dataset, so the team had to build one from scratch.'), False, 'school'),
 ('2025–2026', ('VinBigData', 'Chương trình đào tạo chuyên sâu về thị giác máy tính, xử lý ngôn ngữ tự nhiên, AI tạo sinh và MLOps. Tại đây tham gia đề tài phát hiện phình động mạch nội sọ bằng học sâu.'),
               ('VinBigData', 'An intensive programme in computer vision, natural language processing, generative AI and MLOps, including a project on deep-learning detection of intracranial aneurysms.'), False, 'tower'),
 ('2026–', ('GREEN-X, VinUniversity', 'Trợ lý nghiên cứu. Phụ trách xây dựng NTCoral, bộ dữ liệu ảnh rạn san hô Việt Nam, phối hợp với các nhà sinh học biển.', 'Điều kiện thực địa khắc nghiệt hơn phòng thí nghiệm: thiết bị đặt ngoài biển không phải lúc nào cũng vận hành ổn định, và mỗi lần hỏng hóc buộc nhóm phải xem lại thiết kế.'),
           ('GREEN-X, VinUniversity', 'Research Assistant, responsible for building NTCoral, a Vietnamese coral reef image dataset, together with marine biologists.', 'Field conditions are harsher than the lab: equipment deployed at sea does not always run reliably, and each failure sends the team back to the design.'), False, 'vinuni'),
 ('', ('Chặng tiếp theo', 'Lộ trình đã rõ: thạc sĩ, tiến sĩ rồi sau tiến sĩ ở nước ngoài, sau đó trở về giảng dạy đại học tại Việt Nam. Điều chưa biết là ở trường nào. Hướng chuyên sâu dự kiến là AI trên thiết bị biên (edge AI) phục vụ quan trắc ngoài hiện trường. Chặng đường này còn dài.'),
       ('Next stage', 'The route is clear: a master’s degree, a PhD and a postdoc abroad, then a return to Vietnam to teach at a university. What is not yet known is where. The intended specialisation is edge AI for field monitoring. This stretch is long.'), True, 'goal'),
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
    r = os.path.relpath(to, os.path.dirname(frm) or '.')
    if os.path.basename(r) == 'index.html':  # liên kết về trang chủ không lộ "index.html"
        d = os.path.dirname(r); return (d + '/') if d else './'
    return r
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
    0: [('cert', 'Chứng chỉ sư phạm', 'Teaching certificate'), ('teky', 'Trợ giảng', 'Teaching assistant')],
}
# Tên hiện trên công trình chính của từng giai đoạn
PLACES = {0: ('Trường Đại học FPT', 'FPT University'), 1: ('VinBigData', 'VinBigData'), 2: ('VinUniversity', 'VinUniversity'), 3: ('Giảng dạy đại học tại Việt Nam', 'University teaching in Vietnam')}
# Các mốc đã biết trên chặng tiếp theo (chưa biết ở trường nào)
FUTURE = [('Thạc sĩ', 'Master’s'), ('Tiến sĩ', 'PhD'), ('Sau tiến sĩ', 'Postdoc')]
# Trở ngại trên đường ứng với "khó khăn và bài học" của giai đoạn: holes = ổ gà | flood = ngập nước, cát tràn | rocks = đá lở
OBSTACLE = {0: 'holes', 2: 'flood'}

def stage_json(lang):
    out = []
    for i, (when, vi, en, nx, icon) in enumerate(JOURNEY):
        d = vi if lang == 'vi' else en
        pj = [dict(slug=s, anchor=a, title=E(tv if lang == 'vi' else te)) for s, a, tv, te in STAGE_PROJECTS.get(i, [])]
        ms = [dict(kind=k, label=E(lv if lang == 'vi' else le)) for k, lv, le in MILESTONES.get(i, [])]
        out.append(dict(when=when, title=d[0], paras=[E(d[1])], lesson=E(d[2]) if len(d) > 2 else '', icon=icon, place=PLACES.get(i, ('', ''))[0 if lang == 'vi' else 1], projects=pj, milestones=ms, obstacle=OBSTACLE.get(i, 'holes')))
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
    return f'''<template id="proj-{w['slug']}"><header class="phead"><div class="mono">{t['p_tag']} · {w['year']}</div><h2>{E(title_of(w, lang))}</h2><p>{E(d['sub'])}</p><div class="pact">{"".join(f'<a href="{u}">{E(nm)}</a>' for nm, u in w['links'])}<a class="alt" href="{rel(p, U['workdir'] + w['slug'] + '.html')}">{t['p_page']}</a></div></header>
<dl class="pmeta"><div><dt>{t['role']}</dt><dd>{E(d['role'])}</dd></div><div><dt>{t['where']}</dt><dd>{E(d['where'])}</dd></div><div><dt>{t['status']}</dt><dd>{E(d['status'])}</dd></div></dl>
<div class="prose">{parts}</div></template>'''

def shell(lang, key, path, title, body, extra=''):
    t = T[lang]; other = 'en' if lang == 'vi' else 'vi'
    # trang tương ứng ở ngôn ngữ kia
    if path.startswith(URL[lang]['workdir']): twin = URL[other]['workdir'] + os.path.basename(path)
    else: twin = URL[other][key]
    items = ['journey', 'pubs', 'hl'] + (['notes'] if NOTES else [])  # đã bỏ 'work' và 'about' khỏi thanh điều hướng (vẫn sinh trang để link cũ không hỏng)
    nav = ''.join(f'<a class="item{" on" if k == key else ""}" href="{rel(path, URL[lang][k])}">{t[k]}</a>' for k in items)
    a = lambda p: rel(path, p)
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(t['slogan_plain'])} Aaron (Nguyen Ngoc Gia Ninh), GREEN-X, VinUniversity.">
<link rel="icon" href="{a('assets/clover.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Be+Vietnam+Pro:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a('assets/style.css')}?v={VER}"></head><body>
<header class="nav"><a class="brand" href="{a(URL[lang]['home'])}"><img src="{a('assets/clover.svg')}" alt="">Aaron</a><nav class="links" id="navlinks">{nav}<a class="lang" href="{a(twin)}" hreflang="{other}">{other.upper()}</a></nav><button type="button" class="burger" aria-label="{t['menu']}" aria-expanded="false" aria-controls="navlinks"><i></i><i></i><i></i></button></header>
<main>{body}</main>
<footer class="foot"><div class="wrap"><div class="ftop">
<div class="fc fc1"><a class="fbrand" href="{a(URL[lang]['home'])}"><img src="{a('assets/clover.svg')}" alt=""><span><b>Aaron</b><small>{'Nguyễn Ngọc Gia Ninh' if lang == 'vi' else 'Nguyen Ngoc Gia Ninh'}</small></span></a><p class="fq">{t['slogan']}</p></div>
<div class="fc fc2"><span class="ck">{'Liên hệ' if lang == 'vi' else 'Contact'}</span><div class="fmails"><a class="fm" href="mailto:{EMAIL_WORK}"><i>{t['mail_work']}</i>{EMAIL_WORK}</a><a class="fm" href="mailto:{EMAIL}"><i>{t['mail_me']}</i>{EMAIL}</a></div></div>
<div class="fc fc3"><span class="ck">{'Hồ sơ' if lang == 'vi' else 'Profiles'}</span><nav class="fl"><a href="{a('assets/Aaron_CV.pdf')}">CV <i>↓</i></a><a href="{SCHOLAR}">Google Scholar <i>↗</i></a><a href="https://github.com/Zhaninh">GitHub <i>↗</i></a><a href="{LINKEDIN}">LinkedIn <i>↗</i></a></nav></div>
</div><div class="fbot"><span>© {time.strftime('%Y')} Aaron · <a href="{GREENX}">GREEN-X, VinUniversity</a></span><a class="flang" href="{a(twin)}" hreflang="{other}">{'English' if lang == 'vi' else 'Tiếng Việt'}</a></div></div></footer>
<button type="button" class="totop" aria-label="{'Lên đầu trang' if lang == 'vi' else 'Back to top'}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg></button>
<script src="{a('assets/main.js')}?v={VER}"></script>{extra}</body></html>'''

KEEP = ['GREEN-X, VinUniversity', 'reaches people.', 'đến được với con người.', 'truly meaningful', 'thật sự có ý nghĩa', 'Google Scholar', 'Nguyễn Ngọc Gia Ninh', 'Nguyen Ngoc Gia Ninh']
def nobreak(html):
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<title\b.*?</title>|<textarea\b.*?</textarea>|<[^>]+>)', html, flags=re.S)
    for i, seg in enumerate(parts):
        if not seg or seg.startswith('<'): continue
        for k in KEEP:
            seg = seg.replace(k, '\x00' + k + '\x01')
        seg = re.sub(r'(?<![\w\x00-])(\w+(?:[-‑]\w+)+)(?![\w\x01])', lambda m: '\x00' + m.group(1) + '\x01', seg)
        parts[i] = seg.replace('\x00', '<span class="nw">').replace('\x01', '</span>')
    return ''.join(parts)

def write(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full), exist_ok=True); open(full, 'w').write(nobreak(s) if path.endswith('.html') else s)

def head(t1, p, label=''):
    return f'<section class="page-head"><div class="wrap">{f"<div class=mono>{E(label)}</div>" if label else ""}<h1>{E(t1)}</h1><p>{E(p)}</p></div></section>'

for lang in ('vi', 'en'):
    t = T[lang]; U = URL[lang]
    # ---- trang chủ ----
    p = U['home']; f = next(w for w in WORK if w['star']); fw = f[lang]
    doors = ''.join(f'<a class="row reveal" href="{rel(p, U[k])}"><h3>{t[k]}</h3><p>{E(t["d_" + k])}</p><span class="mono">{n}</span></a>'
                    for k, n in (('journey', f'{len(JOURNEY)}'), ('work', f'{len(WORK)}'), ('about', 'CV')))
    ints = ''.join(f'<li><b>{E(a)}</b><span>{E(d)}</span></li>' for a, d in t['interests'])
    vi_ = lang == 'vi'
    def cov(sl):
        return next((f'assets/projects/{sl}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{sl}.{x}'))), None)
    def sec_head(k, h, more=None):
        m = f'<a class="shead-more" href="{more[0]}">{more[1]} <i>→</i></a>' if more else ''
        return f'<div class="shead reveal"><div><div class="mono">{k}</div><h2>{h}</h2></div>{m}</div>'
    def target(tg):
        if not tg: return None
        return rel(p, U['hl']) + '#' + tg[1] if tg[0] == 'hl' else rel(p, U['workdir'] + tg[1] + '.html')
    nl = ''.join((f'<li class="reveal"><time>{d}</time>' + (f'<a href="{target(tg)}">{E(nv if vi_ else ne)} <i>→</i></a>' if tg else f'<span>{E(nv if vi_ else ne)}</span>') + '</li>') for d, nv, ne, tg in NEWS)
    news_html = f'<section class="news"><div class="wrap">{sec_head("01", "Tin mới" if vi_ else "News")}<ul class="nlist">{nl}</ul></div></section>'
    def rcard(w, big=False):
        d = w[lang]; href = rel(p, U['workdir'] + w['slug'] + '.html'); c = cov(w['slug'])
        img = f'<span class="rc-img"><img src="{rel(p, c)}" alt="" loading="lazy"></span>' if c else ''
        return (f'<a class="rc reveal{" big" if big else ""}" href="{href}">{img}<span class="rc-b"><span class="rc-m"><b>{w["year"]}</b><em>{E(d["status"])}</em></span>'
                f'<span class="rc-t">{E(title_of(w, lang))}</span><span class="rc-s">{E(d["sub"])}</span><span class="rc-r">{E(d["role"])}</span><span class="rc-go">{"Trang dự án" if vi_ else "Project page"} →</span></span></a>')
    others = [w for w in WORK if not w['star']]
    research_html = (f'<section class="research"><div class="wrap">{sec_head("02", "Nghiên cứu" if vi_ else "Research", (rel(p, U["pubs"]), "Tất cả công bố" if vi_ else "All publications"))}'
                     f'{rcard(f, True)}<div class="rgrid">{"".join(rcard(w) for w in others)}</div></div></section>')
    sts = sorted(STORIES, key=lambda x: x[0], reverse=True)[:3]
    def hcard(st):
        iso, dd, pv, pe, tv, te, sv, se, ims, src, tags = st
        return (f'<a class="hc reveal" href="{rel(p, U["hl"])}#{ims[0].split("_")[0]}"><span class="hc-img"><img src="{rel(p, "assets/hl/" + ims[0] + ".webp")}" alt="" loading="lazy"></span>'
                f'<span class="hc-m"><time>{dd}</time> · {E(pv if vi_ else pe)}</span><span class="hc-t">{E(tv if vi_ else te)}</span></a>')
    hl_html = (f'<section class="hlhome"><div class="wrap">{sec_head("05", t["hl"], (rel(p, U["hl"]), "Xem tất cả" if vi_ else "See all"))}'
               f'<div class="hcgrid">{"".join(hcard(x) for x in sts)}</div></div></section>')
    three = f'<script src="{rel(p, "assets/three.min.js")}"></script><script src="{rel(p, "assets/journey3d.js")}?v={VER}"></script>'
    body = f'''<section class="hero"><div class="wrap"><div class="hero-grid"><div class="hero-l">
<div class="hello">{t['hello']}</div>
<h1 class="name">{t['name']}</h1>
<p class="role">{t['role_pre']} <a class="gxt" href="{GREENX}">GREEN-X, VinUniversity</a></p><div class="typed" data-words="{E(json.dumps(t['words'], ensure_ascii=False))}"></div>
<p class="bio">{t['bio']}</p>
<a class="jbtn" href="{rel(p, U['journey'])}"><span class="ji"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 42c0-10 14-8 16-18S14 12 18 6" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="1 6"/><circle cx="18" cy="6" r="4" fill="currentColor"/><circle cx="8" cy="42" r="3" fill="currentColor"/></svg></span><span class="jt"><b>{t['go_journey']}</b><small>{t['j_sub']}</small></span><span class="ja">→</span></a></div>
<figure class="pfig reveal"><div class="portrait"><div class="disc"></div><div class="orbit"><i></i></div><img class="me" src="{rel(p, 'assets/aaron_cut.webp')}" alt="{E(t['name'].replace('<br>', ' '))}" width="760" height="1000"></div></figure></div>
<p class="hslogan reveal"><span>{t['slogan']}</span></p>
<div class="kontakt reveal"><div class="kbar"><a class="km" href="mailto:{EMAIL_WORK}"><span class="kic"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/></svg></span><span class="kk">{t['mail_work']}</span><span class="kv">{EMAIL_WORK}</span></a><i class="ksep"></i><a class="km" href="mailto:{EMAIL}"><span class="kic"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/></svg></span><span class="kk">{t['mail_me']}</span><span class="kv">{EMAIL}</span></a><i class="ksep k2"></i><nav class="kl"><a href="{rel(p, 'assets/Aaron_CV.pdf')}">CV<i>↓</i></a><a href="{SCHOLAR}">Scholar<i>↗</i></a><a href="https://github.com/Zhaninh">GitHub<i>↗</i></a><a href="{LINKEDIN}">LinkedIn<i>↗</i></a></nav></div></div></div></section>
{news_html}
{research_html}
<section class="belief dir"><div class="wrap">{sec_head("03", "Định hướng" if vi_ else "Direction")}<div class="belief-grid"><div class="reveal"><div class="mono">{t['believe']}</div><q>{t['slogan']}</q></div>
<div class="reveal"><div class="mono">{t['h_int']}</div><ol class="ints">{ints}</ol></div></div></div></section>
<section class="teaser-wrap jhome"><div class="wrap">{sec_head("04", t['t_title'])}<a class="teaser reveal" href="{rel(p, U['journey'])}" data-j3d="teaser" data-stages="{stage_json(lang)}"><canvas></canvas><div class="cap"><div class="mono">{len(JOURNEY)} {t['t_n']}</div><p>{E(t['d_journey'])}</p><span class="btn pri">{t['t_btn']}</span></div></a></div></section>
{hl_html}
'''
    write(p, shell(lang, 'home', p, ('Nguyễn Ngọc Gia Ninh (Aaron)' if lang == 'vi' else 'Nguyen Ngoc Gia Ninh (Aaron)') + ' · ' + t['myrole'], body, three))
    # ---- hành trình ----
    p = U['journey']
    lis = ''.join(f'<li class="reveal{" next" if nx else ""}"><div class="mono">{E(when)}</div><div><h3>{E((vi if lang == "vi" else en)[0])}</h3>{"".join(f"<p>{E(x)}</p>" for x in (vi if lang == "vi" else en)[1:])}{"".join(f"<p><a class=link href={rel(p, U['workdir'] + s + '.html')}>{E(tv if lang == 'vi' else te)}</a></p>" for s, a, tv, te in STAGE_PROJECTS.get(i, []))}</div></li>' for i, (when, vi, en, nx, _) in enumerate(JOURNEY))
    wmap = {w['slug']: w for w in WORK}
    tpls = ''.join(proj_template(wmap[s], lang, p) for i in sorted(STAGE_PROJECTS) for s, a, tv, te in STAGE_PROJECTS[i])
    j3d = f'''<section class="j3d" data-j3d="full" style="--n:9" data-stage="{t['p_stage']}" data-more="{t['more']}" data-less="{t['less']}" data-bump="{t['bump']}" data-unknown="{t['unknown']}" data-future="{E(json.dumps([f[0 if lang == 'vi' else 1] for f in FUTURE], ensure_ascii=False))}" data-pin="{t['p_in']}" data-tag="{t['p_tag']}" data-stages="{stage_json(lang)}"><div class="j3d-sticky"><canvas></canvas><div class="j3d-labels"></div>
<article class="j3d-card"><div class="k"></div><h3></h3><div class="tx"></div></article><div class="j3d-hint">{t['hint']}</div></div>
<div class="j3d-panel" aria-hidden="true"><div class="pbar"><button type="button" class="pback">← {t['p_close']}</button><span class="mono pk"></span></div><div class="pbody"></div></div>{tpls}</section>'''
    three = f'<script src="{rel(p, "assets/three.min.js")}"></script><script src="{rel(p, "assets/journey3d.js")}?v={VER}"></script>'
    write(p, shell(lang, 'journey', p, t['journey'] + ' · Aaron', head(t['h_journey'], t['s_journey']) + j3d + f'<section class="path-fallback"><div class="wrap"><ol class="path">{lis}</ol></div></section>', three))
    # ---- công việc ----
    p = U['work']
    onj = {sl for i in STAGE_PROJECTS for sl, *_ in STAGE_PROJECTS[i]}
    def pcard(w):
        d = w[lang]; href = rel(p, U['workdir'] + w['slug'] + '.html')
        jl = f'<a class="pc-j" href="{rel(p, U["journey"])}#{w["slug"]}">{"Xem trên hành trình" if lang == "vi" else "See it on the journey"} <i>↗</i></a>' if w['slug'] in onj else ''
        cov = next((f'assets/projects/{w["slug"]}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{w["slug"]}.{x}'))), None)
        cv = f'<a class="pc-cover" href="{href}" tabindex="-1" aria-hidden="true"><img src="{rel(p, cov)}" alt="" loading="lazy"></a>' if cov else ''
        return (f'<article class="pc reveal{" star" if w["star"] else ""}">{cv}<div class="pc-top"><span class="pc-y">{w["year"]}</span><span class="pc-s">{E(d["status"])}</span></div>'
                f'<h3><a href="{href}">{E(title_of(w, lang))}</a></h3><p>{E(d["sub"])}</p>'
                f'<div class="pc-meta"><span>{E(d["role"])}</span><span>{E(d["where"])}</span></div>'
                f'<div class="pc-act"><a class="pc-go" href="{href}">{"Chi tiết dự án" if lang == "vi" else "Project page"} <i>→</i></a>{jl}</div></article>')
    cards = ''.join(pcard(w) for w in WORK)
    write(p, f'<!DOCTYPE html><meta charset="utf-8"><title>{t["pubs"]}</title><meta http-equiv="refresh" content="0;url={rel(p, U["pubs"])}"><link rel="canonical" href="{rel(p, U["pubs"])}"><a href="{rel(p, U["pubs"])}">{t["pubs"]}</a>')
    for w in WORK:
        d = w[lang]; p = U['workdir'] + w['slug'] + '.html'
        parts, lk = proj_parts(w, lang)
        body = head(title_of(w, lang), d['sub'], w['year']) + f'''<section><div class="wrap split"><div class="prose reveal">{parts}<p style="margin-top:48px"><a class="link" href="{rel(p, U['pubs'])}">{'← Công bố' if lang == 'vi' else '← Publications'}</a></p></div>
<aside class="box"><h4>{t['role']}</h4><div>{E(d['role'])}</div><h4>{t['where']}</h4><div>{E(d['where'])}</div><h4>{t['status']}</h4><div>{E(d['status'])}</div><h4>{t['links']}</h4>{lk}</aside></div></section>'''
        write(p, shell(lang, 'pubs', p, title_of(w, lang) + ' · Aaron', body))
    # ---- công bố ----
    p = U['pubs']
    def cov_of(sl):
        return next((f'assets/projects/{sl}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{sl}.{x}'))), None)
    def pub(y, st, ti, au, vv, ve, u, sl):
        href = rel(p, U['workdir'] + sl + '.html') if sl else None; cv = cov_of(sl) if sl else None
        th = f'<a class="pth" href="{href}" tabindex="-1" aria-hidden="true"><img src="{rel(p, cv)}" alt="" loading="lazy"></a>' if cv else '<span class="pth"></span>'
        tt = f'<a class="t" href="{href}">{E(ti)}</a>' if href else f'<div class="t">{E(ti)}</div>'
        acts = (f'<a class="pgo" href="{href}">{"Trang dự án" if lang == "vi" else "Project page"} <i>→</i></a>' if href else '') + (f'<a class="pdoi" href="{u}">DOI <i>↗</i></a>' if u else '')
        return f'<li class="reveal{" star" if st else ""}">{th}<div><span class="mono">{y}</span>{tt}<div class="a">{au}</div><div class="v">{E(vv if lang == "vi" else ve)}</div><div class="pacts">{acts}</div></div></li>'
    lis = ''.join(pub(*x) for x in PUBS)
    write(p, shell(lang, 'pubs', p, t['pubs'] + ' · Aaron', head(t['h_pubs'], t['s_pubs']) + f'<section><div class="wrap"><ol class="pubs">{lis}</ol></div></section>'))
    # ---- dấu ấn ----
    p = U['hl']
    def story(st):
        iso, dd, pv, pe, tv, te, sv, se, ims, src, tags = st
        def ar(x):
            try:
                from PIL import Image as _I
                w_, h_ = _I.open(os.path.join(ROOT, 'assets/hl', x + '.webp')).size; return w_ / h_
            except Exception: return 4 / 3
        def btn(x): a_ = ar(x); return f'<button type="button" class="hg-i{' pt' if a_ < 1 else ''}" style="--ar:{a_:.4f}" data-full="{rel(p, "assets/hl/" + x + ".webp")}"><img src="{rel(p, "assets/hl/" + x + ".webp")}" alt="" loading="lazy"></button>'
        im = ''.join(btn(x) for x in ims)
        tg = ''.join(f'<span>{E(x if lang == "vi" else TAG_EN.get(x, x))}</span>' for x in tags)
        sl = ''.join(f'<a href="{u}" rel="noopener">{"Bài gốc" if lang == "vi" else "Original post"} · {E(n)} <i>↗</i></a>' for n, u in src)
        return (f'<article class="hs reveal" id="{ims[0].split("_")[0]}"><div class="hb"><div class="hb-l"><div class="hm"><time datetime="{iso}">{dd}</time><span>{E(pv if lang == "vi" else pe)}</span></div><h3>{E(tv if lang == "vi" else te)}</h3><div class="ht">{tg}</div></div>'
                f'<div class="hb-r"><p>{E(sv if lang == "vi" else se)}</p><div class="hsrc">{sl}</div></div></div><div class="hg n{len(ims)}">{im}</div></article>')
    sts = sorted(STORIES, key=lambda x: x[0], reverse=True)
    body = head(t['h_hl'], t['s_hl']) + f'<section class="hl-wrap"><div class="wrap"><div class="hl-list">{"".join(story(x) for x in sts)}</div></div></section><div class="lb" hidden><button type="button" class="lb-x" aria-label="Close">×</button><img alt=""></div>'
    write(p, shell(lang, 'hl', p, t['hl'] + ' · Aaron', body))
    # ---- giới thiệu ----
    p = U['about']
    parts = ''.join(f'<h2>{E(h)}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in ps) for h, ps in ABOUT[lang])
    body = head(t['h_about'], t['s_about']) + f'''<section><div class="wrap split"><div class="prose reveal">{parts}</div>
<aside class="box"><h4>CV</h4><div><a class="link" href="{rel(p, 'assets/Aaron_CV.pdf')}">{t['cv']}</a></div><h4>{t['contact']}</h4><div><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></div></aside></div></section>'''
    write(p, shell(lang, 'about', p, t['about'] + ' · Aaron', body))

open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
# README.md được viết tay, build.py không ghi đè
print('ok')
