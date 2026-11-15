import re
#!/usr/bin/env python3
"""Trang cá nhân Aaron. Tĩnh, song ngữ (vi mặc định ở gốc, en trong /en/).
Thêm nội dung: thêm một mục vào WORK / PUBS / JOURNEY / NOTES rồi chạy `python3 build.py`.
Mục có "star": True sẽ tự nổi lên (trang chủ lấy mục WORK có star đầu tiên)."""
import os, html, json, time, math
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
            slogan='Công nghệ thật sự có ý nghĩa<br class="sb"> khi nó <em>đến được với con người.</em>', slogan_plain='Công nghệ thật sự có ý nghĩa khi nó đến được với con người.',
            who='Tôi là <b>Nguyễn Ngọc Gia Ninh</b>, thường gọi là Aaron, nghiên cứu viên AI tại GREEN-X, VinUniversity. Tôi xây dữ liệu và hệ thống thị giác máy tính cho những bài toán gần với con người: trước là người bệnh, nay là biển.',
            hello='Xin chào, tôi là', name='Nguyễn Ngọc<br>Gia Ninh', myrole='Trợ lý nghiên cứu · GREEN-X, VinUniversity', role_pre='Trợ lý nghiên cứu tại', mail_work='Công việc', mail_me='Cá nhân', words=['trí tuệ nhân tạo ứng dụng', 'thị giác máy tính', 'AI trên thiết bị biên', 'IoT và AIoT', 'tên thường gọi: Aaron'],
            interests=[('Thị giác máy tính', 'Nhận dạng, phân vùng và hiểu ảnh, video trong điều kiện thực tế.'), ('Dữ liệu và đánh giá', 'Xây dựng, kiểm chứng dữ liệu và quy trình đánh giá mô hình.'), ('AI trên thiết bị biên', 'Đưa mô hình về chạy trên thiết bị ngoài hiện trường.'), ('IoT và AIoT', 'Kết nối cảm biến, thiết bị với mô hình AI để thu thập dữ liệu và ra quyết định tại hiện trường.')], h_int='hướng quan tâm', featured='đề tài tiêu biểu',
            bio='Tôi nghiên cứu <span class="ri">trí tuệ nhân tạo ứng dụng</span>, trọng tâm là <span class="ri">thị giác máy tính</span>, với mong muốn đưa kết quả nghiên cứu vào các bài toán thực tế tại Việt Nam.',
            go_journey='Đi cùng tôi qua hành trình', j_sub='Bản đồ 3D: các giai đoạn, dự án và chặng phía trước', c_label='liên hệ', believe='quan điểm nghiên cứu', now='đang thực hiện', t_title='Hành trình nghiên cứu', t_btn='Xem hành trình', t_n='giai đoạn', bump='khó khăn và bài học', hint='cuộn xuống để đi tiếp ↓', unknown='chưa xác định', p_in='dự án trong chặng này', p_tag='dự án', p_stage='giai đoạn', menu='Mục lục', more='Xem thêm', less='Thu gọn', p_close='Quay lại hành trình', p_page='Mở trang riêng của dự án',
            doing='đang thực hiện', read='Xem đề tài', role='Vai trò', where='Nơi thực hiện', status='Trạng thái', links='Minh chứng', nolinks='Sẽ bổ sung khi kết quả được công bố.',
            back='Tất cả đề tài', cv='Lý lịch khoa học (PDF)', contact='Liên hệ',
            d_journey='Quá trình học tập, nghiên cứu và định hướng sắp tới.', d_work='Các đề tài đã có công bố, bộ dữ liệu hoặc mã nguồn công khai.', d_about='Thế mạnh, hạn chế đang khắc phục, lý lịch khoa học và liên hệ.',
            h_journey='Hành trình nghiên cứu', s_journey='Các giai đoạn học tập và nghiên cứu từ năm 2021 đến nay, cùng định hướng sắp tới.',
            h_work='Dự án', s_work='Toàn bộ dự án tôi đã và đang làm. Mỗi dự án có trang riêng, và có thể xem nó nằm ở đâu trên hành trình.',
            h_hl='Dấu ấn', s_hl='Những chuyến công tác, sự kiện và khoảnh khắc trên đường đi. Mỗi tấm ảnh đi kèm câu chuyện của nó.', h_pubs='Công bố', s_pubs='Thứ tự tác giả ghi theo nhà xuất bản hoặc kho lưu trữ.',
            h_about='Giới thiệu', s_about='Tôi làm nghiên cứu ứng dụng về trí tuệ nhân tạo và định hướng theo con đường nghiên cứu, giảng dạy đại học.'),
 'en': dict(home='Home', journey='Journey', work='Projects', pubs='Publications', hl='Highlights', about='About', notes='Notes',
            slogan='Technology is truly meaningful<br class="sb"> when it <em>reaches people.</em>', slogan_plain='Technology is truly meaningful when it reaches people.',
            who='I am <b>Nguyen Ngoc Gia Ninh</b>, known as Aaron, an AI researcher at GREEN-X, VinUniversity. I build datasets and computer vision systems for problems close to people: first patients, now the sea.',
            hello='Hello, I am', name='Nguyen Ngoc<br>Gia Ninh', myrole='Research Assistant · GREEN-X, VinUniversity', role_pre='Research Assistant at', mail_work='Work', mail_me='Personal', words=['applied artificial intelligence', 'computer vision', 'edge AI', 'IoT and AIoT', 'also known as Aaron'],
            interests=[('Computer vision', 'Recognition, segmentation and understanding of images and video under real-world conditions.'), ('Data and evaluation', 'Building and validating datasets and model evaluation protocols.'), ('Edge AI', 'Running models on devices deployed in the field.'), ('IoT and AIoT', 'Connecting sensors and devices with AI models to collect data and make decisions in the field.')], h_int='research interests', featured='featured project',
            bio='I work on <span class="ri">applied artificial intelligence</span> with a focus on <span class="ri">computer vision</span>, aiming to bring research results to real-world problems in Vietnam.',
            go_journey='Take the journey with me', j_sub='A 3D map of stages, projects and the road ahead', c_label='contact', believe='research outlook', now='in progress', t_title='Research journey', t_btn='See the journey', t_n='stages', bump='difficulties and lessons', hint='scroll down to continue ↓', unknown='not yet known', p_in='projects in this stage', p_tag='project', p_stage='stage', menu='Menu', more='More', less='Less', p_close='Back to the journey', p_page='Open the project page',
            doing='in progress', read='View project', role='Role', where='Where', status='Status', links='Evidence', nolinks='Links will appear when results are public.',
            back='All projects', cv='Download CV (PDF)', contact='Contact',
            d_journey='Study, research and the plan ahead.', d_work='Projects with a publication, dataset or public code.', d_about='Strengths, current limitations, CV and contact.',
            h_journey='Research journey', s_journey='Stages of study and research since 2021, and the plan ahead.',
            h_work='Projects', s_work='Every project I have worked on. Each has its own page, and you can see where it sits on the journey.',
            h_hl='Highlights', s_hl='Field trips, events and moments along the way. Every photo comes with its story.', h_pubs='Publications', s_pubs='Author order as listed by the publisher or repository.',
            h_about='About', s_about='I work on applied AI and am on my way to becoming a researcher and university lecturer.'),
}
URL = {'en': dict(home='index.html', journey='journey.html', work='work.html', pubs='publications.html', hl='highlights.html', about='about.html', notes='notes.html', workdir='work/', mdir='mentors/'),  # tiếng Anh là mặc định (ở gốc)
       'vi': dict(home='vi/index.html', journey='vi/hanh-trinh.html', work='vi/cong-viec.html', pubs='vi/cong-bo.html', hl='vi/dau-an.html', about='vi/gioi-thieu.html', notes='vi/ghi-chep.html', workdir='vi/cong-viec/', mdir='vi/nguoi-huong-dan/')}

WORK = [  # rank: thứ hạng 'độ mạnh' của dự án; 4 dự án đầu lên trang chủ

 dict(slug='ntcoral', impact=dict(status='in_prep', role='first', active=True), star=True, title='NTCoral', year='2025–',
  vi=dict(sub='Bộ dữ liệu ảnh rạn san hô Việt Nam, trích từ video khảo sát dưới nước và được gán nhãn cùng chuyên gia sinh học biển.',
          dek='Bộ dữ liệu ảnh rạn san hô Việt Nam có nhãn và mặt nạ phân vùng được kiểm chứng',
          role='Phụ trách dữ liệu; tác giả thứ nhất của bài báo đang chuẩn bị', where='GREEN-X, VinUniversity', status='Đang thực hiện',
          body=[('Đặt vấn đề', ['Phần lớn bộ dữ liệu san hô công khai được thu ở các vùng biển khác. Ảnh rạn san hô Việt Nam có nhãn còn rất ít, nên chưa thể biết các mô hình hiện có hoạt động ra sao trên dữ liệu trong nước, và cần bao nhiêu nhãn tại chỗ.'], []),
                ('Tiến độ', ['Khoảng 2.000 ảnh đã được trích chọn từ video khảo sát. Mặt nạ phân vùng và nhãn cấp chi đang được thực hiện cùng chuyên gia sinh học biển. Trang này sẽ được cập nhật khi bài báo dữ liệu hoàn thành.'], []),
                ('Phần việc đảm nhận', [], ['Phụ trách quy trình từ video khảo sát đến ảnh: rà soát video, chọn khung hình, kiểm tra chất lượng.', 'Thiết kế cách chọn khung hình: loại ảnh gần trùng, sàng lọc chất lượng, giữ độ phủ giữa các điểm khảo sát.', 'Chuẩn bị dữ liệu và quy trình để gán nhãn cùng chuyên gia.']),
                ('Quy trình', [], ['Video khảo sát', 'Chọn khung hình', 'Kiểm tra chất lượng', 'Mặt nạ và nhãn chi', 'Chuyên gia kiểm chứng', 'Bộ dữ liệu mở'])]),
  en=dict(sub='An image dataset of Vietnamese coral reefs, extracted from underwater survey video and labelled with marine biologists.',
          dek='A Vietnamese coral-reef image dataset with expert-verified labels and masks',
          role='Data lead; first author of the paper in preparation', where='GREEN-X, VinUniversity', status='In progress',
          body=[('Why it matters', ['Public coral datasets come mostly from other regions. Vietnamese reefs have very few labelled images, so it is unclear how far existing models transfer and how many local labels are needed.'], []),
                ('Progress', ['About 2,000 images have been extracted from survey video. Segmentation masks and genus-level labels are under way with marine biologists. This page will be updated when the data paper is complete.'], []),
                ('What I do', [], ['Lead the pipeline from survey video to images: video review, frame selection, quality checks.', 'Design frame selection: remove near-duplicates, screen quality, keep coverage across survey sites.', 'Prepare data and workflow for expert annotation.']),
                ('Pipeline', [], ['Survey video', 'Frame selection', 'Quality checks', 'Masks and genus labels', 'Expert verification', 'Open dataset'])]),
  links=[]),
 dict(slug='vlr', impact=dict(status='preprint', role='coauthor', dataset=True, dois=['10.22541/au.177368999.91959735/v1', '10.5281/zenodo.19709456'], zenodo=['19709456']), star=False, title_vi='Nhận dạng tiếng nói qua khẩu hình tiếng Việt', title_en='Vietnamese lip reading', year='2024–2026',
  vi=dict(sub='Tiếng Việt có sáu thanh điệu, nhiều âm tiết khác thanh nhưng gần như cùng khẩu hình. VLR là bộ dữ liệu đọc khẩu hình tiếng Việt quy mô lớn, kèm một quy trình cải tiến đưa tỉ lệ lỗi từ xuống 29,5%.', dek='Bộ dữ liệu và quy trình nhận dạng tiếng nói qua hình ảnh cho tiếng Việt', teaser_cap='Quy trình xây dựng VLR: tách âm thanh và hình; Whisper nhận dạng lời thoại theo từng từ; MediaPipe tìm khuôn mặt rồi cắt vùng môi. Nguồn: tiền ấn phẩm, CC BY 4.0.', stats=[('116.000', 'đoạn video'), ('198', 'giờ nói'), ('1.794', 'video nguồn'), ('29,5%', 'WER tốt nhất')],
          role='Tìm nguồn dữ liệu và thực nghiệm mô hình cơ sở; khóa luận tốt nghiệp', where='Đại học FPT · VSB – Đại học Kỹ thuật Ostrava (Cộng hoà Séc) · Đại học Mở TP. Hồ Chí Minh', status='Tiền ấn phẩm · Dữ liệu trên Zenodo',
          body=[('Đặt vấn đề', ['Đọc khẩu hình (nhận dạng tiếng nói qua hình ảnh) là bài toán chuyển chuyển động môi, hàm và nét mặt thành chữ, không cần âm thanh. Kỹ thuật này có thể hỗ trợ người khiếm thính và người mất khả năng phát âm.', 'Tiếng Việt khó với bài toán này: có sáu thanh điệu, nhiều âm tiết khác thanh nhưng gần như cùng khẩu hình. Trước VLR, tiếng Việt chưa có bộ dữ liệu đọc khẩu hình quy mô lớn.'], []),
                ('Bộ dữ liệu', ['VLR được xây từ 1.794 video thuộc 25 danh sách phát YouTube tiếng Việt công khai, chọn những đoạn thấy rõ mặt người nói và nói tự nhiên. Âm thanh được nhận dạng bằng Whisper để lấy lời thoại có mốc thời gian từng từ; khuôn mặt được tìm bằng MediaPipe và cắt vùng môi.'],
                 ['Khoảng 116.000 đoạn video, 198 giờ nói, 65,6 GB.', 'Chia 178 giờ để huấn luyện, 10 giờ để kiểm định, 10 giờ để kiểm thử.', 'Phát hành trên Zenodo, giấy phép CC BY 4.0.'], ('vlr_strip', 'Mười lăm khung hình liên tiếp của vùng môi trong một đoạn video.')),
                ('Tổ chức dữ liệu', ['Bộ dữ liệu chia thành bảy phần (PART1–PART7) để dễ tải về. Mỗi đoạn câu nằm trong một thư mục riêng; mỗi từ trong câu có một video đã bỏ tiếng và một file CSV ghi thời điểm bắt đầu và kết thúc của từ.'], [],
                 (('vlr_tree', 'vlr_csv'), 'Trái: cấu trúc thư mục của VLR, từ gốc (a) đến file video và CSV (e). Phải: một file nhãn, mỗi dòng là một từ kèm mốc thời gian.')),
                ('Thống kê', ['Thanh ngang (không dấu) chiếm nhiều nhất, thanh ngã ít nhất. Các đoạn video phần lớn dài từ 4 đến 6 giây. Những từ thường gặp nhất là các hư từ như "là", "cái", "có", "của".'], [],
                 (('vlr_tone', 'vlr_dur', 'vlr_words'), 'Từ trái sang: số từ theo sáu thanh điệu; độ dài các đoạn video; 30 từ xuất hiện nhiều nhất. Nguồn: tiền ấn phẩm, CC BY 4.0.')),
                ('Kết quả', ['Sáu mô hình đọc khẩu hình chỉ dùng hình ảnh được tinh chỉnh và đánh giá trên VLR. AV-HuBERT cho kết quả tốt nhất, với tỉ lệ lỗi từ (WER) 62,18% khi giải mã thông thường.', 'Nhóm đề xuất thêm bốn bước cải tiến: ghép mô hình ngôn ngữ 5-gram tiếng Việt, lọc mẫu khó rồi học theo lộ trình (curriculum learning), căn chỉnh vùng môi, và xếp hạng lại N kết quả tốt nhất bằng một bộ giải mã Transformer gọn. Nhờ vậy WER trên tập kiểm thử giảm còn 29,5%.'],
                 [], ('table', (['Mô hình', 'WER cơ sở', 'WER sau cải tiến'], [['AV-HuBERT', '62,18%', '29,5%'], ['Auto-AVSR', '69,88%', '36,9%'], ['LipNet', '75,13%', '42,8%'], ['VSP-LLM', '81,59%', '47,2%']], 0))),
                ('Ứng dụng thử nghiệm', ['Nhóm làm một ứng dụng desktop để thử đọc khẩu hình ngoài phòng thí nghiệm. Người dùng chọn một video có sẵn hoặc quay trực tiếp bằng webcam. Khung hình được tiền xử lý bằng OpenCV và MediaPipe trên GPU, sau đó mô hình LipNet (TensorFlow) dự đoán câu nói. Ứng dụng chạy trên NVIDIA Jetson Nano.'], [],
                 (('vlr_app', 'vlr_appflow'), 'Trái: ứng dụng đọc một video và trả về câu "sẽ cùng cô chuyển sang"; video lấy từ YouTube công khai, mắt người nói đã được che. Phải: luồng xử lý của ứng dụng.')),
                ('Phần việc đảm nhận', [], ['Tìm và chọn nguồn video YouTube tiếng Việt cho bộ dữ liệu.', 'Huấn luyện và đánh giá các mô hình cơ sở VSP-LLM và Auto-AVSR.'])]),
  en=dict(sub='Vietnamese has six tones, and many syllables that differ only in tone look almost the same on the lips. VLR is a large-scale Vietnamese lip-reading dataset with a refined pipeline that brings word error rate down to 29.5%.', dek='A dataset and visual speech recognition pipeline for Vietnamese', teaser_cap='VLR construction: audio and video are split; Whisper transcribes word by word; MediaPipe finds the face and the lips are cropped. Source: preprint, CC BY 4.0.', stats=[('116,000', 'clips'), ('198', 'hours of speech'), ('1,794', 'source videos'), ('29.5%', 'best WER')],
          role='Data sourcing and baseline experiments; capstone thesis', where='FPT University · VSB – Technical University of Ostrava · Ho Chi Minh City Open University', status='Preprint · Dataset on Zenodo',
          body=[('Why it matters', ['Lip reading (visual speech recognition) turns lip, jaw and facial motion into text without audio. It can support deaf people and people who have lost their voice.', 'Vietnamese is hard for this task: it has six tones, and many syllables that differ only in tone look almost the same on the lips. Before VLR there was no large-scale Vietnamese lip-reading dataset.'], []),
                ('The dataset', ['VLR is built from 1,794 videos in 25 public Vietnamese YouTube playlists, chosen for a clear view of the speaker and natural speech. Whisper transcribes the audio with word-level timestamps; MediaPipe finds the face and the lip region is cropped.'],
                 ['About 116,000 clips, 198 hours of speech, 65.6 GB.', '178 hours for training, 10 for validation, 10 for testing.', 'Released on Zenodo under CC BY 4.0.'], ('vlr_strip', 'Fifteen consecutive frames of the lip region from one clip.')),
                ('How the data is organised', ['The dataset is split into seven parts (PART1–PART7) for easier download. Each utterance has its own folder; each word in it has a silent video and a CSV file with the word’s start and end time.'], [],
                 (('vlr_tree', 'vlr_csv'), 'Left: folder structure of VLR, from the root (a) to the video and CSV files (e). Right: one label file, one word per line with its timestamps.')),
                ('Statistics', ['The level tone (no mark) is the most frequent and the tilde tone the least. Most clips last 4 to 6 seconds. The most common words are function words such as "là", "cái", "có", "của".'], [],
                 (('vlr_tone', 'vlr_dur', 'vlr_words'), 'Left to right: word count by the six tones; clip duration; the 30 most frequent words. Source: preprint, CC BY 4.0.')),
                ('Results', ['Six visual-only lip-reading models were fine-tuned and evaluated on VLR. AV-HuBERT was best, with a word error rate (WER) of 62.18% under greedy decoding.', 'The team added four refinements: shallow fusion with a Vietnamese 5-gram language model, difficulty filtering with curriculum learning, lip-region alignment, and N-best re-ranking with a lightweight Transformer decoder. Together they bring test WER down to 29.5%.'],
                 [], ('table', (['Model', 'Baseline WER', 'Refined WER'], [['AV-HuBERT', '62.18%', '29.5%'], ['Auto-AVSR', '69.88%', '36.9%'], ['LipNet', '75.13%', '42.8%'], ['VSP-LLM', '81.59%', '47.2%']], 0))),
                ('Demo application', ['The team built a desktop application to try lip reading outside the lab. The user picks a video or records one from a webcam. Frames are pre-processed with OpenCV and MediaPipe on the GPU, then a LipNet model (TensorFlow) predicts the sentence. The application runs on an NVIDIA Jetson Nano.'], [],
                 (('vlr_app', 'vlr_appflow'), 'Left: the application reads a video and returns the sentence "sẽ cùng cô chuyển sang"; the video comes from public YouTube and the speaker’s eyes are covered. Right: the application’s processing flow.')),
                ('What I did', [], ['Found and selected Vietnamese YouTube video sources for the dataset.', 'Trained and evaluated VSP-LLM and Auto-AVSR baselines.'])]),
  teaser='vlr_pipeline', bib='''@article{quoc2026vlr,
  title   = {A Large-Scale Vietnamese Lip Reading Dataset and Enhanced Recognition Pipeline},
  author  = {Quoc, Trung Nguyen and Thao, Nguyen Pham Thi and Ninh, Nguyen Ngoc Gia and Quynh, Hoa Dam Nguyen and Hoang, Vinh Truong and Bilik, S. and Sindelar, Matej and Stefansky, J. and Martinek, R. and Bilik, P.},
  journal = {Authorea Preprints},
  year    = {2026},
  doi     = {10.22541/au.177368999.91959735/v1}
}''',
  links=[('Zenodo', 'https://doi.org/10.5281/zenodo.19709456'), ('Preprint', 'https://doi.org/10.22541/au.177368999.91959735/v1')]),
 dict(slug='aquaculture', impact=dict(status='under_review', role='coauthor', dois=['10.13140/RG.2.2.24130.95688']), star=False, title_vi='Ra quyết định tự động trong nuôi trồng thuỷ sản thông minh', title_en='Autonomous decision-making in smart aquaculture', year='2026',
  teaser='aq_suda',
  vi=dict(sub='Một bài tổng quan cấp hệ thống, xếp các nghiên cứu nuôi trồng thuỷ sản thông minh theo khung Cảm nhận – Hiểu – Quyết định – Hành động (SUDA), từ giám sát thụ động đến điều khiển vòng kín.',
          dek='From Monitoring to Action: tổng quan về ra quyết định tự động trong nuôi trồng thuỷ sản thông minh',
          teaser_cap='Khung SUDA: cảm biến môi trường, hình ảnh và âm thanh; học máy và dung hợp dữ liệu; bộ ra quyết định; và lớp trí tuệ giám sát (bản sao số, mô hình ngôn ngữ lớn). Nguồn: tiền ấn phẩm, CC BY 4.0.',
          stats=[('4', 'khâu SUDA'), ('3', 'họ bộ ra quyết định'), ('4', 'tầng thời gian điều khiển'), ('11', 'tác giả')],
          role='Viết Mục 6: Ra quyết định tự động và điều khiển vòng kín', where='GREEN-X và Viện Kỹ thuật và Khoa học Máy tính, VinUniversity · Viện Công nghệ Thông tin, ĐHQG Hà Nội · Trinity College Dublin', status='Tiền ấn phẩm · Đang bình duyệt',
          body=[('Đặt vấn đề', ['Nhu cầu thuỷ sản tăng nhanh, trong khi môi trường nuôi biến động theo từng giờ: một lần cho ăn có thể làm oxy hoà tan, amoniac và pH thay đổi ngay trong ngày. Phần lớn hệ thống hiện nay mới dừng ở giám sát và dự báo, tức là hỗ trợ con người ra quyết định chứ chưa tự hành động.', 'Bài tổng quan nhìn toàn bộ chuỗi từ cảm biến đến cơ cấu chấp hành, và hỏi: cần gì để một trang trại đi từ giám sát sang tự vận hành một cách an toàn?'], []),
                ('Khung SUDA', ['Các nghiên cứu được xếp vào bốn khâu của một vòng kín. Cách xếp này cho thấy chỗ nào đã chín, chỗ nào còn đứt gãy giữa các khâu.'], ['Cảm nhận: cảm biến chất lượng nước, camera dưới nước, thuỷ âm.', 'Hiểu: học máy, học sâu, dung hợp đa nguồn, AI tại biên.', 'Quyết định: luật và hệ chuyên gia, chính sách học được, học tăng cường.', 'Hành động: cho ăn, sục khí, thay nước, quản lý sức khoẻ đàn cá.']),
                ('Mục 6: Ra quyết định và điều khiển vòng kín', ['Đây là phần tôi viết. Mục này trả lời hai câu hỏi: trạng thái mà mô hình ước lượng được chuyển thành hành động điều khiển ra sao, và khi nào nên dùng luật cố định, chính sách học được, học tăng cường hay để con người can thiệp.', 'Ba họ bộ ra quyết định được so sánh theo mức minh bạch, khả năng thích nghi và rủi ro khi triển khai. Một lớp trọng tài hành động đứng giữa, gộp nhiều tiêu chí, kiểm tra ràng buộc an toàn rồi mới cho phép tác động lên trang trại.'],
                 ['Từ dự báo đến quyết định: một trạng thái dự báo có thể cần những phản ứng khác nhau tuỳ rủi ro sinh học, chi phí năng lượng và độ tin cậy của cảm biến.', 'Luật và hệ chuyên gia: dễ kiểm tra, chạy được tại chỗ khi mất kết nối, nhưng kém thích nghi khi mùa vụ, cảm biến hay sinh khối thay đổi.', 'Chính sách học được: tách phần nhận thức khỏi phần điều khiển, đưa phần tối ưu nặng về chạy ngoại tuyến.', 'Học tăng cường: hợp với các mục tiêu có độ trễ như hệ số chuyển đổi thức ăn, nhưng cần môi trường mô phỏng và giới hạn an toàn trước khi chạy trên trang trại thật.', 'Con người trong vòng lặp: tự động hoá theo mức độ tin cậy, có rào chắn an toàn và quyền can thiệp của người vận hành.'],
                 ('aq_decision', 'Ngăn xếp ra quyết định: dữ liệu đa nguồn đi qua ba họ bộ ra quyết định, rồi qua lớp trọng tài hành động trước khi điều khiển trang trại. Nguồn: tiền ấn phẩm, CC BY 4.0.'),
                 ('aq_hierarchy', 'Bốn tầng thời gian: điều khiển an toàn (giây–phút), vận hành (phút–giờ), tối ưu sinh học (ngày–tuần) và lập kế hoạch (cả vụ nuôi). Nguồn: tiền ấn phẩm, CC BY 4.0.')),
                ('Phần việc đảm nhận', [], ['Viết toàn bộ Mục 6: tổng hợp tài liệu, lập luận và cấu trúc cho năm tiểu mục từ 6.1 đến 6.5.'])]),
  en=dict(sub='A system-level survey that organises smart-aquaculture research along a Sense–Understand–Decide–Act (SUDA) loop, from passive monitoring to closed-loop control.',
          dek='From Monitoring to Action: a survey of autonomous decision-making in smart aquaculture',
          teaser_cap='The SUDA framework: environmental, visual and acoustic sensing; learning and data fusion; decision engines; and a supervisory layer (digital twins, large language models). Source: preprint, CC BY 4.0.',
          stats=[('4', 'SUDA stages'), ('3', 'decision paradigms'), ('4', 'control timescales'), ('11', 'authors')],
          role='Wrote Section 6, Autonomous Decision-Making and Closed-Loop Control', where='GREEN-X and College of Engineering and Computer Science, VinUniversity · Information Technology Institute, VNU Hanoi · Trinity College Dublin', status='Preprint · Under review',
          body=[('Why it matters', ['Demand for aquatic food is rising fast, while farm conditions shift within hours: a single feeding can move dissolved oxygen, ammonia and pH the same day. Most systems still stop at monitoring and forecasting; they support people rather than act.', 'The survey looks at the whole chain from sensor to actuator and asks what a farm needs to move from monitoring to safe autonomous operation.'], []),
                ('The SUDA framework', ['Studies are placed on the four stages of a closed loop, which shows where the field is mature and where the links between stages break.'], ['Sense: water-quality probes, underwater cameras, hydro-acoustics.', 'Understand: machine learning, deep learning, multimodal fusion, edge AI.', 'Decide: rules and expert systems, learned policies, reinforcement learning.', 'Act: feeding, aeration, water exchange, health management.']),
                ('Section 6: decision-making and closed-loop control', ['This is the section I wrote. It asks how estimated farm states turn into control actions, and when to use fixed rules, learned policies, reinforcement learning or human intervention.', 'The three decision paradigms are compared on transparency, adaptability and deployment risk. An action-arbitration layer sits between them and the farm, combining criteria and checking safety constraints before any action is taken.'],
                 ['From prediction to decision: the same predicted state may call for different responses depending on biological risk, energy cost and sensor reliability.', 'Rules and expert systems: auditable and able to run locally when connectivity drops, but slow to adapt to seasons, sensor drift or biomass growth.', 'Learned policies: separate perception from control and move heavy optimisation offline.', 'Reinforcement learning: suited to delayed outcomes such as feed conversion, but needs simulation and safety limits before running on a live farm.', 'Human in the loop: graded autonomy with safety guardrails and operator override.'],
                 ('aq_decision', 'Decision stack: multimodal inputs pass through three decision paradigms and an action-arbitration layer before farm control. Source: preprint, CC BY 4.0.'),
                 ('aq_hierarchy', 'Four timescales: safety-critical control (seconds–minutes), operations (minutes–hours), biological optimisation (days–weeks) and planning (whole cycle). Source: preprint, CC BY 4.0.')),
                ('What I did', [], ['Wrote all of Section 6: literature synthesis, argument and structure of subsections 6.1 to 6.5.'])]),
  links=[('Preprint', 'https://doi.org/10.13140/RG.2.2.24130.95688')]),
 dict(slug='vnplant', impact=dict(status='unpublished', role='core'), star=False, title_vi='Phân loại cây thuốc Việt Nam', title_en='Vietnamese medicinal plant classification', year='2025',
  vi=dict(sub='Đánh giá nhiều mô hình học sâu trên bộ ảnh 255 loài cây thuốc Việt Nam.', role='Huấn luyện và đánh giá mô hình', where='Đại học FPT · cùng Đàm Nguyễn Quỳnh Hoa và Phạm Thị Thảo Nguyên', status='Dự án nhóm, không công bố',
          body=[('Bối cảnh', ['VNPlant-200 (Nguyễn Quốc Trung và Trương Hoàng Vinh, 2021) là bộ ảnh công khai đầu tiên về 200 loài cây thuốc Việt Nam. Nhóm chúng tôi mở rộng bộ này thành VNPlant-255: thêm 55 loài, tổng cộng khoảng 34.800 ảnh chụp ngoài thực địa, với ánh sáng, nền và góc chụp thay đổi tự nhiên.', 'Mục tiêu là một bộ chuẩn đánh giá cho bài toán phân loại chi tiết: so sánh mạng tích chập, Transformer, mô hình lai và mô hình gọn nhẹ trong cùng một cấu hình.'], []),
                ('Cách đánh giá', [], ['Chia 80/10/10 cho huấn luyện, kiểm định, kiểm thử, giữ tỉ lệ từng loài.', 'Cùng độ phân giải 224 px, cùng kích thước lô, 20 epoch cho mọi mô hình.', 'Ghi lại độ chính xác, số tham số và chi phí tính toán để xét khả năng triển khai.']),
                ('Phần việc đảm nhận', [], ['Huấn luyện và đánh giá bảy họ mô hình: ConvNeXtV2-Tiny, MaxViT-Tiny, CoAtNet-0, SwinV2-Tiny, Xception, Xception kết hợp MIGT, và YOLOv8 phân loại.', 'Quản lý dữ liệu, trọng số và nhật ký huấn luyện của nhóm trên Kaggle.']),
                ('Ghi chú', ['Nhóm quyết định không công bố bài báo. Ảnh của 200 loài gốc thuộc VNPlant-200 nên không được phát hành lại ở đây.'], [])]),
  en=dict(sub='Benchmarking deep learning models on 255 Vietnamese medicinal plant species.', role='Model training and evaluation', where='FPT University · with Dam Nguyen Quynh Hoa and Pham Thi Thao Nguyen', status='Team project, not published',
          body=[('Context', ['VNPlant-200 (Nguyen Quoc Trung and Truong Hoang Vinh, 2021) was the first public image set of 200 Vietnamese medicinal plant species. Our team extended it to VNPlant-255: 55 more species, about 34,800 field photographs in total, with natural variation in light, background and viewpoint.', 'The goal was a benchmark for fine-grained classification, comparing CNNs, Transformers, hybrid and lightweight models under one setup.'], []),
                ('Evaluation setup', [], ['80/10/10 train/validation/test split, stratified by species.', 'Same 224 px resolution, batch size and 20 epochs for every model.', 'Accuracy, parameter count and compute cost recorded to judge deployability.']),
                ('What I did', [], ['Trained and evaluated seven model families: ConvNeXtV2-Tiny, MaxViT-Tiny, CoAtNet-0, SwinV2-Tiny, Xception, Xception with MIGT, and YOLOv8 classification.', 'Managed the team’s data, weights and training logs on Kaggle.']),
                ('Note', ['The team decided not to publish the paper. Images of the original 200 species belong to VNPlant-200 and are not redistributed here.'], [])]),
  links=[]),
 dict(slug='marine', impact=dict(status='system', role='support', active=True), star=False, title_vi='Nuôi biển thông minh', title_en='Smart marine aquaculture', year='2025–',
  vi=dict(sub='Hệ thống giám sát tự động cho nuôi biển: camera dưới nước, thuỷ âm và cảm biến chất lượng nước, triển khai từ phòng thí nghiệm đến lồng nuôi ngoài khơi.',
          dek='Giám sát nuôi biển bằng AI tại biên, từ bể thí nghiệm đến lồng nổi ở vịnh Nha Phu',
          stats=[('4', 'giai đoạn triển khai'), ('5', 'thông số chất lượng nước'), ('5', 'đơn vị đối tác')],
          role='Hỗ trợ thiết kế web/ứng dụng và hạ tầng VPN', where='GREEN-X, VinUniversity · Học viện Nông nghiệp Việt Nam · Viện Nghiên cứu Nuôi trồng Thuỷ sản I và III · Đại học Nha Trang', status='Đang thực hiện',
          body=[('Đặt vấn đề', ['Môi trường nuôi biển khắc nghiệt: nước đục, sinh vật bám làm mờ ống kính, muối ăn mòn thiết bị và nguồn điện ngoài khơi hạn chế. Theo dõi liên tục mà không cần lặn kiểm tra thủ công là yêu cầu cốt lõi.'], []),
                ('Hệ thống', [], ['Cảm biến: oxy hoà tan, pH, nhiệt độ, độ mặn, độ đục; camera dưới nước và mảng thuỷ âm.', 'AI tại biên ước lượng sinh khối, phân cụm đàn cá, mức bám bẩn ống kính và phân tích âm thanh khi cá ăn.', 'Dữ liệu truyền qua MQTT mã hoá và 4G/LTE về máy chủ, lưu chuỗi thời gian và ảnh, hiển thị trên bảng điều khiển của GREEN-X.', 'Trạm ngoài khơi chạy bằng điện mặt trời có pin dự phòng.']),
                ('Các giai đoạn triển khai', [], ['05.2025: thử nghiệm trong phòng thí nghiệm tại Học viện Nông nghiệp Việt Nam, Hà Nội.', '08.2025: bể xi măng trong nhà tại Viện Nghiên cứu Nuôi trồng Thuỷ sản I, Hải Phòng.', '03.2026: lồng nổi ngoài khơi tại vịnh Nha Phu, Nha Trang.', '05.2026: bể tròn ngoài trời tại Viện Nghiên cứu Nuôi trồng Thuỷ sản III, Nha Trang.']),
                ('Phần việc đảm nhận', [], ['Hỗ trợ thiết kế giao diện web và ứng dụng.', 'Hỗ trợ thiết lập VPN cho hạ tầng hệ thống.'])]),
  en=dict(sub='Automated monitoring for marine aquaculture: underwater cameras, hydrophones and water-quality sensors, deployed from the lab to offshore cages.',
          dek='Edge-AI monitoring of fish farming, from lab tanks to floating cages in Nha Phu Bay',
          stats=[('4', 'deployment phases'), ('5', 'water-quality parameters'), ('5', 'partner institutions')],
          role='Supported web/app design and VPN infrastructure', where='GREEN-X, VinUniversity · Vietnam National University of Agriculture · Research Institutes for Aquaculture I and III · Nha Trang University', status='Ongoing',
          body=[('Why it matters', ['Sea farming is harsh on equipment: turbid water, biofouling on lenses, salt corrosion and limited offshore power. Continuous monitoring without manual diving is the core requirement.'], []),
                ('The system', [], ['Sensors: dissolved oxygen, pH, temperature, salinity, turbidity; underwater cameras and hydrophone arrays.', 'Edge AI estimates biomass, school clustering, lens fouling and feeding sounds.', 'Data travels over encrypted MQTT and 4G/LTE to servers, stored as time series and media, and shown on the GREEN-X dashboard.', 'The offshore station runs on solar power with battery backup.']),
                ('Deployment phases', [], ['05.2025: lab trials at the Vietnam National University of Agriculture, Hanoi.', '08.2025: indoor raceways at the Research Institute for Aquaculture I, Hai Phong.', '03.2026: offshore floating cages in Nha Phu Bay, Nha Trang.', '05.2026: outdoor circular tanks at the Research Institute for Aquaculture III, Nha Trang.']),
                ('What I did', [], ['Supported web and app interface design.', 'Supported VPN setup for the system infrastructure.'])]),
  links=[('Chi tiết dự án', 'https://hoang-pm-7604119.github.io/myself/projects/smart-marine-aquaculture/')]),
 dict(slug='coralcons', impact=dict(status='system', role='support', active=True), star=False, title_vi='Giám sát bảo tồn rạn san hô vịnh Nha Trang', title_en='Coral reef conservation monitoring, Nha Trang Bay', year='2025–',
  vi=dict(sub='Trạm quan trắc chạy bằng điện mặt trời và cụm cảm biến đặt tại rạn san hô, ghi liên tục chất lượng nước để phát hiện sớm điều kiện gây tẩy trắng.',
          dek='Quan trắc liên tục rạn san hô bằng trạm năng lượng mặt trời và cảm biến dưới nước',
          stats=[('24/7', 'ghi dữ liệu liên tục'), ('5', 'thông số chất lượng nước'), ('4', 'đơn vị đối tác')],
          role='Hỗ trợ thiết kế web/ứng dụng và hạ tầng VPN', where='GREEN-X, VinUniversity · Ban Quản lý Vịnh Nha Trang · Đại học Nha Trang', status='Đang thực hiện',
          body=[('Đặt vấn đề', ['Rạn san hô vịnh Nha Trang chịu tác động của nhiệt độ nước biển tăng, ô nhiễm từ bờ và biến động độ mặn. Các đợt lặn khảo sát định kỳ dễ bỏ lỡ những cú sốc ngắn, như oxy hoà tan giảm đột ngột, vốn có thể gây tẩy trắng.'], []),
                ('Hệ thống', [], ['Cụm cảm biến đặt ở độ sâu rạn: oxy hoà tan, nhiệt độ, pH, độ mặn, độ đục.', 'Trạm điện mặt trời gắn trên phao tiêu hàng hải, vỏ kín chuẩn IP68.', 'Dữ liệu truyền qua mạng di động có mã hoá, cung cấp theo thời gian thực cho nhà khoa học và kiểm lâm biển.', 'Ảnh dưới nước và ảnh flycam được gắn toạ độ cùng dữ liệu chất lượng nước.']),
                ('Phần việc đảm nhận', [], ['Hỗ trợ thiết kế giao diện web và ứng dụng.', 'Hỗ trợ thiết lập VPN cho hạ tầng hệ thống.'])]),
  en=dict(sub='A solar-powered station and reef-depth sensor clusters log water quality around the clock, to catch conditions that trigger bleaching early.',
          dek='Continuous reef monitoring with a solar station and underwater sensors',
          stats=[('24/7', 'continuous logging'), ('5', 'water-quality parameters'), ('4', 'partner institutions')],
          role='Supported web/app design and VPN infrastructure', where='GREEN-X, VinUniversity · Nha Trang Bay Management Board · Nha Trang University', status='Ongoing',
          body=[('Why it matters', ['Reefs in Nha Trang Bay face rising sea temperature, coastal runoff and salinity swings. Periodic dive surveys miss short shocks, such as sudden drops in dissolved oxygen, that can trigger bleaching.'], []),
                ('The system', [], ['Sensor clusters at reef depth: dissolved oxygen, temperature, pH, salinity, turbidity.', 'A solar station on a navigation beacon, with IP68-sealed housings.', 'Encrypted cellular telemetry gives real-time feeds to scientists and park rangers.', 'Underwater and drone imagery is georeferenced with the water-quality data.']),
                ('What I did', [], ['Supported web and app interface design.', 'Supported VPN setup for the system infrastructure.'])]),
  links=[('Chi tiết dự án', 'https://hoang-pm-7604119.github.io/myself/projects/coral-reef-conservation-nha-trang/')]),
 dict(slug='aneurysm', impact=dict(status='published', role='coauthor', dois=['10.1201/9781003667360-21']), star=False, title_vi='Phát hiện phình động mạch nội sọ', title_en='Intracranial aneurysm detection', year='2026',
  vi=dict(sub='Phình động mạch nội sọ gặp ở khoảng 3% dân số và dễ bị bỏ sót khi nhỏ. Chương sách đề xuất một quy trình học sâu hai giai đoạn để phát hiện và định vị túi phình trên ảnh mạch máu não.',
          dek='Quy trình học sâu nhiều giai đoạn trên dữ liệu RSNA Intracranial Aneurysm',
          stats=[('~3%', 'dân số có phình mạch nội sọ'), ('2', 'giai đoạn'), ('3D', 'CTA · MRA · MRI'), ('15', 'trang chương sách')],
          role='Đồng tác giả', where='Chương sách trong Intelligent Precision Healthcare · CRC Press, 2026', status='Chương sách · CRC Press',
          body=[('Đặt vấn đề', ['Phình động mạch nội sọ là chỗ phình cục bộ của mạch máu não. Khi vỡ, túi phình gây xuất huyết trong sọ. CTA, MRA và MRI đều phổ biến, nhưng túi phình nhỏ hoặc khó thấy đôi khi vẫn bị bỏ sót, kể cả với bác sĩ có kinh nghiệm.', 'Các phương pháp có máy tính hỗ trợ hướng tới phát hiện sớm hơn và ổn định hơn giữa các lần đọc.'], []),
                ('Phương pháp', ['Quy trình gồm hai giai đoạn, chạy trên nhiều phương thức ảnh của bộ dữ liệu RSNA Intracranial Aneurysm.'], ['Giai đoạn 1: một mạng 3D U-Net phân vùng các vùng mạch máu nghi ngờ với độ nhạy cao, để không bỏ sót tổn thương.', 'Giai đoạn 2: các khối 3D quanh vùng nghi ngờ được phân loại bằng 3D ResNet, bộ mã hoá U-Net hoặc một mạng 3D CNN gọn nhẹ, để xác định có túi phình hay không và vị trí giải phẫu.']),
                ('Kết quả', ['Theo chương sách, quy trình hai giai đoạn cải thiện độ chính xác chẩn đoán, độ ổn định và hiệu quả quy trình làm việc. Khi tích hợp vào thực hành lâm sàng như một công cụ hỗ trợ quyết định, nó có thể giúp bác sĩ chẩn đoán hình ảnh phát hiện túi phình sớm hơn.'], [])]),
  en=dict(sub='Intracranial aneurysms affect about 3% of people and small ones are easy to miss. The chapter proposes a two-stage deep learning pipeline to detect and localise aneurysms on brain vascular imaging.',
          dek='A multistage deep learning pipeline on the RSNA Intracranial Aneurysm dataset',
          stats=[('~3%', 'of people have one'), ('2', 'stages'), ('3D', 'CTA · MRA · MRI'), ('15', 'pages')],
          role='Co-author', where='Chapter in Intelligent Precision Healthcare · CRC Press, 2026', status='Book chapter · CRC Press',
          body=[('Why it matters', ['An intracranial aneurysm is a local bulge in a brain blood vessel; if it ruptures, it bleeds inside the skull. CTA, MRA and MRI are routine, yet small or subtle aneurysms are sometimes missed even by experienced radiologists.', 'Computer-assisted methods aim at earlier and more consistent detection.'], []),
                ('Method', ['A two-stage pipeline across the imaging modalities of the RSNA Intracranial Aneurysm dataset.'], ['Stage 1: a 3D U-Net segments candidate vascular regions with high sensitivity, so lesions are not missed.', 'Stage 2: 3D patches around each candidate are classified by a 3D ResNet, a U-Net encoder or a lightweight 3D CNN, for aneurysm presence and anatomical site.']),
                ('Results', ['The chapter reports that the two-stage pipeline improves diagnostic accuracy, robustness and workflow efficiency. Used as decision support, it may help radiologists find aneurysms earlier.'], [])]),
  links=[('DOI', 'https://doi.org/10.1201/9781003667360-21')]),
]


# ---- thứ hạng dự án: tính tự động từ trạng thái, vai trò và số liệu tác động (data/metrics.json) ----
SCORE_W = dict(
    status={'published': 3.0, 'under_review': 2.0, 'preprint': 1.5, 'in_prep': 1.0, 'system': 1.0, 'unpublished': 0.0},
    role={'first': 2.5, 'core': 1.0, 'coauthor': 0.5, 'support': 0.25},
    dataset=1.5,      # có bộ dữ liệu công khai
    active=1.0,       # dự án đang thực hiện
    citations=1.0,    # × log(1 + số trích dẫn)
    downloads=0.5,    # × log(1 + lượt tải duy nhất / 100)
    stars=0.5,        # × log(1 + số sao GitHub)
)
try:
    METRICS = json.load(open(os.path.join(ROOT, 'data', 'metrics.json'), encoding='utf-8'))
except Exception:
    METRICS = {}

def impact_score(w):
    im = w.get('impact', {}); m = METRICS.get(w['slug'], {}); W_ = SCORE_W
    return (W_['status'].get(im.get('status'), 0) + W_['role'].get(im.get('role'), 0)
            + (W_['dataset'] if im.get('dataset') else 0) + (W_['active'] if im.get('active') else 0)
            + W_['citations'] * math.log1p(m.get('citations', 0)) + W_['downloads'] * math.log1p(m.get('downloads', 0) / 100)
            + W_['stars'] * math.log1p(m.get('stars', 0)) + im.get('pin', 0))

RANKED = sorted(WORK, key=impact_score, reverse=True)

PUBS = [  # (năm, star, tiêu đề, tác giả, nơi_vi, nơi_en, link, dự án)
 ('2026', False, 'A Multistage Deep Learning Approach for Intracranial Aneurysm Detection', f'N. P. T. Thao, {ME}, T. N. Quoc, V. T. Hoang', 'Chương sách, Intelligent Precision Healthcare, CRC Press, tr. 287–301', 'Book chapter, Intelligent Precision Healthcare, CRC Press, pp. 287–301', 'https://doi.org/10.1201/9781003667360-21', 'aneurysm'),
 ('2026', False, 'From Monitoring to Action: A Comprehensive Survey of Autonomous Decision-Making in Smart Aquaculture Systems', f'Q.-H. N. Dam, P. H. Nguyen, M. P. Tran, C.-S. Trinh, T. T. Nguyen, {ME}, et al.', 'Tiền ấn phẩm; đang bình duyệt tại Computers and Electronics in Agriculture', 'Preprint; under review at Computers and Electronics in Agriculture', 'https://doi.org/10.13140/RG.2.2.24130.95688', 'aquaculture'),
 ('2026', False, 'A Large-Scale Vietnamese Lip Reading Dataset and Enhanced Recognition Pipeline', f'T. N. Quoc, N. P. T. Thao, {ME}, H. D. N. Quynh, V. T. Hoang, S. Bilik, M. Sindelar, J. Stefansky, R. Martinek, P. Bilik', 'Tiền ấn phẩm', 'Preprint', 'https://doi.org/10.22541/au.177368999.91959735/v1', 'vlr'),
]

PUB_LINKS = {'vlr': [('Bộ dữ liệu', 'Dataset', 'https://doi.org/10.5281/zenodo.19709456')]}  # link phụ của một công bố

FB_TA = 'Phan Thục Anh (Facebook)'; FB_GX = 'GREEN-X (Facebook)'
STORIES = [  # (ngày ISO, ngày hiển thị, nơi_vi, nơi_en, tiêu đề_vi, tiêu đề_en, tóm tắt_vi, tóm tắt_en, [ảnh], [(nhãn, link)], [thẻ])
 ('2023-09-05', '09–12.2023', 'Quy Nhơn, Bình Định', 'Quy Nhon, Binh Dinh',
  'Thực tập tại FPT AI Creative Valley', 'Internship at FPT AI Creative Valley',
  'Tháng 9/2023, tôi cùng 52 sinh viên Đại học FPT đến Quy Nhơn thực tập tại FPT AI Creative Valley (AI Valley). Trong ba tháng, tôi làm AI Intern và tham gia ba dự án. Dự án đầu tiên phân tích đánh giá của người dùng tiếng Việt bằng PhoBERT và XLM-R. Hai dự án còn lại là một ứng dụng Smart Menu và một bộ dữ liệu chữ viết tay tiếng Việt cho cuộc thi OCR. Tấm ảnh trong phòng làm việc là do tôi chụp, nên trong ảnh không có tôi.',
  'In September 2023, I went to Quy Nhon with 52 FPT University students for an internship at FPT AI Creative Valley (AI Valley). For three months I worked as an AI Intern on three projects. The first analysed Vietnamese user reviews with PhoBERT and XLM-R. The other two were a Smart Menu application and a Vietnamese handwriting dataset for an OCR competition. I took the photo in the office, so I am not in it.',
  ['aivalley_1', 'aivalley_2', 'aivalley_3', 'aivalley_4', 'aivalley_5', 'aivalley_6', 'aivalley_0'], [('Facebook', 'https://www.facebook.com/share/1M2dTchPix/'), ('Facebook', 'https://www.facebook.com/share/p/1FQpTYngum/')], ['FPT AI Valley', 'Quy Nhơn']),
 ('2026-10-25', '24–26.10.2026', 'Nha Trang, Khánh Hòa', 'Nha Trang, Khanh Hoa',
  'Gian triển lãm GREEN-X tại Ngày hội Chuyển đổi số', 'GREEN-X booth at the Digital Transformation Expo',
  'GREEN-X mang đến Ngày hội các giải pháp cho đô thị xanh, du lịch bền vững, nuôi biển và bảo tồn biển. Robot đại dương phát triển cùng VinaTech là điểm dừng chân đông khách nhất.',
  'GREEN-X brought solutions for green cities, sustainable tourism, mariculture and marine conservation to the expo. The ocean robot built with VinaTech drew the biggest crowd.',
  ['expo_0', 'expo_1'], [(FB_GX, 'https://www.facebook.com/share/p/19jbPiY6e9/')], ['GREEN-X', 'Khánh Hòa']),
 ('2026-07-01', '07.2026', 'Nha Trang và Vân Phong, Khánh Hòa', 'Nha Trang and Van Phong, Khanh Hoa',
  'Trở lại Khánh Hòa: du lịch xanh, Hòn Mun và nuôi biển', 'Back in Khanh Hoa: green tourism, Hon Mun and mariculture',
  'Chuyến công tác nối tiếp Cần Giờ. Đoàn làm việc với Sở Văn hóa, Thể thao và Du lịch về Bộ tiêu chuẩn Du lịch Xanh và chuẩn bị hạ thủy hệ thống IoT quan trắc đa dạng sinh học ở Hòn Mun. Sau đó, đoàn thăm trang trại cá chẽm công nghệ cao của Australis ở Vân Phong để bàn hướng AI cho nuôi biển.',
  'A trip right after Can Gio. The team met the provincial tourism department about the Green Tourism standard and prepared to deploy the IoT biodiversity-monitoring system at Hon Mun. They then visited Australis’ high-tech sea-bass farm at Van Phong to discuss AI for mariculture.',
  ['nhatrang_0', 'nhatrang_1'], [(FB_TA, 'https://www.facebook.com/share/p/14zHYMXiH5c/')], ['Công tác', 'IoT']),
 ('2026-06-20', '06.2026', 'Cần Giờ, TP. Hồ Chí Minh', 'Can Gio, Ho Chi Minh City',
  'Khảo sát rừng ngập mặn Cần Giờ', 'Surveying the Can Gio mangroves',
  'Làm việc với Ban Quản lý rừng phòng hộ Cần Giờ và khảo sát thực địa. GREEN-X giới thiệu hệ thống bảo tồn rừng ngập mặn kết hợp viễn thám, IoT, AI và digital twin, với mục tiêu chung là biến Cần Giờ thành một living lab về công nghệ bảo tồn.',
  'Meetings and a field survey with the Can Gio protection-forest board. GREEN-X presented a mangrove conservation system combining remote sensing, IoT, AI and a digital twin, with the shared aim of making Can Gio a living lab for conservation technology.',
  ['cangio_0', 'cangio_1', 'cangio_2'], [(FB_TA, 'https://www.facebook.com/share/p/19k7V5EHyh/')], ['Công tác', 'Thực địa']),
 ('2026-06-10', '06.2026', 'VinUniversity, Hà Nội', 'VinUniversity, Hanoi',
  'VinUni Research Day', 'VinUni Research Day',
  'Gian GREEN-X giới thiệu các dự án chính sách qua poster và video. Phần công nghệ được trưng bày trực tiếp, gồm nền tảng quan sát cá theo thời gian thực ở Nha Trang và robot đại dương vừa bơi vừa bay.',
  'The GREEN-X booth presented its policy projects through posters and video. The technology was shown in person, including a live fish-watching platform from Nha Trang and an ocean robot that both swims and flies.',
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
TAG_EN = {'Quy Nhơn': 'Quy Nhon', 'Cột mốc': 'Milestone', 'Công tác': 'Field trip', 'Thực địa': 'Fieldwork', 'Sự kiện': 'Event'}

NEWS = [  # (ngày hiển thị, nội dung_vi, nội dung_en, đích: ('hl', id) | ('work', slug) | None)
 ('10.2026', 'GREEN-X giới thiệu các giải pháp chuyển đổi xanh tại Ngày hội Chuyển đổi số Khánh Hòa 2026.', 'GREEN-X presented its green-transformation solutions at Khanh Hoa Digital Transformation Day 2026.', ('hl', 'expo')),
 ('04.2026', 'Chính thức là trợ lý nghiên cứu tại GREEN-X, VinUniversity.', 'Started as a research assistant at GREEN-X, VinUniversity.', None),
 ('2026', 'Chương sách về phát hiện phình động mạch nội sọ được xuất bản trong Intelligent Precision Healthcare (CRC Press).', 'Book chapter on intracranial aneurysm detection published in Intelligent Precision Healthcare (CRC Press).', ('work', 'aneurysm')),
 ('2026', 'Bộ dữ liệu đọc khẩu hình tiếng Việt quy mô lớn được phát hành trên Zenodo.', 'Large-scale Vietnamese lip-reading dataset released on Zenodo.', ('work', 'vlr')),
]

MENTOR_CARD = {  # chức danh, đơn vị hiện tại của thầy (vi, en) · và vai trò của thầy đối với tôi: (vai trò vi, vai trò en, nơi, năm bắt đầu, năm kết thúc hoặc None)
 'phung-manh-duong': (('Trợ lý Giáo sư, VinUniversity', 'Assistant Professor, VinUniversity'), [('Người hướng dẫn (PI)', 'Supervisor (PI)', 'GREEN-X, VinUniversity', '2026', None)]),
 'dinh-van-dung': (('Nghiên cứu viên cao cấp, Đại học Quốc gia Hà Nội', 'Senior Researcher, Vietnam National University, Hanoi'), [('Đồng chủ nhiệm (Co-PI)', 'Co-PI', 'GREEN-X, VinUniversity', '2026', None)]),
 'do-danh-cuong': (('Trợ lý Giáo sư, VinUniversity', 'Assistant Professor, VinUniversity'), [('Đồng chủ nhiệm (Co-PI)', 'Co-PI', 'GREEN-X, VinUniversity', '2026', None)]),
}

MENTORS = [
 dict(slug='phung-manh-duong', photo='duong',
  guided=[('ntcoral', 'Chủ trì dự án (PI).', 'Principal investigator of the project.')],
  vi=dict(name='TS. Phùng Mạnh Dương', title='Trợ lý Giáo sư ngành AI và Robotics, Viện Kỹ thuật và Khoa học Máy tính, VinUniversity', role='Người hướng dẫn trực tiếp; Chủ nhiệm (PI) · GREEN-X', short='Trợ lý Giáo sư · AI và Robotics', lead='Nghiên cứu hệ tự hành, UAV và thị giác máy tính cho robot, với hơn 15 năm giảng dạy và nghiên cứu, trong đó gần một thập kỷ tại Úc.', facts=['Tiến sĩ, ĐHQG Hà Nội', 'Sau tiến sĩ, UTS', 'IEEE Senior Member', 'Ba giải Best Paper'],
          bio='Trợ lý Giáo sư ngành AI và Robotics tại Viện Kỹ thuật và Khoa học Máy tính (CECS), VinUniversity; thành viên cấp cao (Senior Member) của IEEE. Trước khi về VinUni, thầy giảng dạy và nghiên cứu nhiều năm tại University of Technology Sydney và Western Sydney University.',
          edu=['Tiến sĩ Kỹ thuật Điện tử, Đại học Quốc gia Hà Nội (2015)', 'Sau tiến sĩ ngành Cơ điện tử, University of Technology Sydney (2017)'],
          areas='Hệ tự hành và trí tuệ nhân tạo; UAV; thị giác máy tính cho robot; SLAM, lập kế hoạch đường đi và điều khiển chuyển động; trí tuệ bầy đàn và IoT.',
          awards=['Best Paper Award, ICCRI (2024)', 'Best Paper Award, Applied Soft Computing, Elsevier (2023)', 'Best Paper Award, ACRA (2019)', 'Endeavour Research Fellowship, Chính phủ Úc (2015)'],
          withme='Người định hướng nghiên cứu của tôi tại GREEN-X: thầy theo sát từng dự án, từ lúc đặt bài toán đến khi công bố.'),
  en=dict(name='Dr. Phung Manh Duong', title='Assistant Professor in AI and Robotics, College of Engineering and Computer Science, VinUniversity', role='Direct supervisor; Principal investigator (PI) · GREEN-X', short='Assistant Professor · AI and Robotics', lead='Works on autonomous systems, UAVs and robot vision, with more than fifteen years of teaching and research, nearly a decade of it in Australia.', facts=['PhD, VNU Hanoi', 'Postdoc, UTS', 'IEEE Senior Member', 'Three Best Paper Awards'],
          bio='Assistant Professor in AI and Robotics at the College of Engineering and Computer Science (CECS), VinUniversity, and a Senior Member of IEEE. Before joining VinUni he taught and researched for many years at the University of Technology Sydney and Western Sydney University.',
          edu=['PhD in Electronic Engineering, Vietnam National University, Hanoi (2015)', 'Postdoc in Mechatronic Engineering, University of Technology Sydney (2017)'],
          areas='Autonomous systems and AI; UAVs; robot vision; SLAM, path planning and motion control; swarm intelligence and IoT.',
          awards=['Best Paper Award, ICCRI (2024)', 'Best Paper Award, Applied Soft Computing, Elsevier (2023)', 'Best Paper Award, ACRA (2019)', 'Endeavour Research Fellowship, Australian Government (2015)'],
          withme='The person who sets the direction of my research at GREEN-X, following each project from framing the problem to publication.'),
  emails=['duong.pm@vinuni.edu.vn'],
  links=[('GREEN-X', 'https://greenx.vinuni.edu.vn/people/phung-manh-duong/'), ('VinUniversity', 'https://vinuni.edu.vn/?p=140853'), ('Homepage', 'https://sites.google.com/view/manhduongphung'),
         ('Google Scholar', 'https://scholar.google.com/citations?user=JE-a1MkAAAAJ&hl=en'), ('ORCID', 'https://orcid.org/0000-0001-5247-6180'), ('arXiv', 'https://arxiv.org/a/phung_m_1.html')]),
 dict(slug='dinh-van-dung', photo='dung', org=('Viện Công nghệ Thông tin · Đại học Quốc gia Hà Nội', 'Information Technology Institute · Vietnam National University, Hanoi'), guided=[],
  vi=dict(name='TS. Đinh Văn Dũng', title='Nghiên cứu viên cao cấp, Viện Công nghệ Thông tin, ĐHQG Hà Nội', role='Đồng chủ nhiệm (Co-PI) · GREEN-X', short='Nghiên cứu viên cao cấp · ĐHQG Hà Nội',
          lead='Nghiên cứu chuyển đổi số và nền tảng số (điện toán đám mây, IoT, MLOps), với ứng dụng trong giáo dục, y tế, nông nghiệp thông minh và chuyển đổi xanh.',
          facts=['Tiến sĩ, Học viện Công nghệ Bưu chính Viễn thông', 'Thạc sĩ, University of Technology Sydney', 'Học giả Fulbright, New York University'], bio='', edu=[], areas='', awards=[], withme=''),
  en=dict(name='Dr. Dinh Van Dzung', title='Senior Researcher, Information Technology Institute, Vietnam National University, Hanoi', role='Co-principal investigator (Co-PI) · GREEN-X', short='Senior Researcher · VNU Hanoi',
          lead='Works on digital transformation and digital platforms (cloud, IoT, MLOps), applied to education, health, smart agriculture and green transformation.',
          facts=['PhD, Posts and Telecommunications Institute of Technology', 'MEE, University of Technology Sydney', 'Fulbright Scholar, New York University'], bio='', edu=[], areas='', awards=[], withme=''),
  emails=['dzung.dinh@vnu.edu.vn', 'dung.dv@vinuni.edu.vn'],
  links=[('GREEN-X', 'https://greenx.vinuni.edu.vn/people/dinh-van-dung/')]),
 dict(slug='do-danh-cuong', photo='cuong',
  guided=[],
  vi=dict(name='TS. Đỗ Danh Cường', title='Trợ lý Giáo sư, Viện Kỹ thuật và Khoa học Máy tính, VinUniversity', role='Đồng chủ nhiệm (Co-PI) · GREEN-X', short='Trợ lý Giáo sư · MESSI Lab', lead='Nghiên cứu cảm biến MEMS, hệ thống năng lượng và AI cho tín hiệu y sinh; từng là nghiên cứu viên tại University of Cambridge.', facts=['Tiến sĩ, Cork Institute of Technology', 'Nghiên cứu viên, University of Cambridge', 'Phụ trách MESSI Lab'],
          bio='Trợ lý Giáo sư tại Viện Kỹ thuật và Khoa học Máy tính (CECS), VinUniversity, phụ trách MESSI Lab (Multidisciplinary Exploration for Sustainable Systems and Intelligence). Trước đó thầy là nghiên cứu viên tại Khoa Kỹ thuật, University of Cambridge (2013–2017).',
          edu=['Cử nhân Điện tử, Đại học Quốc gia Hà Nội (2004)', 'Thạc sĩ Điện tử và Bán dẫn, Chungbuk National University, Hàn Quốc (2007)', 'Tiến sĩ Kỹ thuật Điện tử, Cork Institute of Technology, Ireland (2012)'],
          areas='Cảm biến MEMS và mạch tiêu thụ năng lượng thấp; thu hoạch năng lượng và mạng cảm biến không dây; tối ưu lưới điện thông minh và trạm sạc xe điện; AI cho tín hiệu y sinh (ECG) và chẩn đoán tại chỗ.',
          awards=[],
          withme='Đồng chủ nhiệm các dự án tại GREEN-X, nơi tôi làm trợ lý nghiên cứu.'),
  en=dict(name='Dr. Do Danh Cuong', title='Assistant Professor, College of Engineering and Computer Science, VinUniversity', role='Co-principal investigator (Co-PI) · GREEN-X', short='Assistant Professor · MESSI Lab', lead='Works on MEMS sensors, energy systems and AI for biomedical signals; formerly a research associate at the University of Cambridge.', facts=['PhD, Cork Institute of Technology', 'Research Associate, University of Cambridge', 'Leads the MESSI Lab'],
          bio='Assistant Professor at the College of Engineering and Computer Science (CECS), VinUniversity, where he leads the MESSI Lab (Multidisciplinary Exploration for Sustainable Systems and Intelligence). He was previously a research associate in the Engineering Department, University of Cambridge (2013–2017).',
          edu=['BS in Electronics, Vietnam National University, Hanoi (2004)', 'MEng in Electronics and Semiconductor, Chungbuk National University, Korea (2007)', 'PhD in Electronics Engineering, Cork Institute of Technology, Ireland (2012)'],
          areas='MEMS sensors and low-power circuits; energy harvesting and wireless sensor networks; smart-grid and EV-charging optimisation; AI for biomedical signals (ECG) and point-of-care diagnostics.',
          awards=[],
          withme='Co-principal investigator of the projects at GREEN-X, where I work as a research assistant.'),
  emails=['cuong.dd@vinuni.edu.vn'],
  links=[('GREEN-X', 'https://greenx.vinuni.edu.vn/people/do-danh-cuong/'), ('VinUniversity', 'https://research.vinuni.edu.vn/person/do-cuong-danh/'), ('MESSI Lab', 'https://sites.google.com/view/messi-lab'),
         ('Google Scholar', 'https://scholar.google.com/citations?user=_NdIi4AAAAAJ&hl=en'), ('ORCID', 'https://orcid.org/0000-0003-4785-4524'), ('dblp', 'https://dblp.org/pid/27/10702')]),
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
    2: [('ntcoral', 'buoy', 'NTCoral', 'NTCoral'), ('coralcons', 'office', 'Bảo tồn rạn san hô', 'Coral reef conservation'), ('marine', 'tent', 'Nuôi biển thông minh', 'Smart marine aquaculture')],
}
# CỘT MỐC: việc có thật nhưng không phải dự án và không phải giai đoạn (vật thể nhỏ, nhãn nhỏ, không bấm được)
#   (vật thể: cert = chứng chỉ | teky = lớp học nhỏ, nhãn vi, nhãn en)
MILESTONES = {
    0: [('valley', 'FPT AI Valley', 'FPT AI Valley'), ('cert', 'Chứng chỉ sư phạm', 'Teaching certificate'), ('teky', 'Trợ giảng', 'Teaching assistant')],
}
# NỘI DUNG khi xe đi qua / khi bấm vào cột mốc và công trình phụ: kind -> (vi(tiêu đề, thời gian, đoạn), en(...), liên kết hoặc None)
SPOT_TEXT = {
    'valley': (('FPT AI Creative Valley, Quy Nhơn', '09–12.2023', 'Ba tháng thực tập vị trí AI Intern cùng 52 sinh viên Đại học FPT. Tôi tham gia ba dự án: phân tích đánh giá của người dùng tiếng Việt bằng PhoBERT và XLM-R, ứng dụng Smart Menu, và bộ dữ liệu chữ viết tay tiếng Việt. Đây là lần đầu tôi làm AI trong một nhóm sản phẩm thật.'),
               ('FPT AI Creative Valley, Quy Nhon', '09–12.2023', 'A three-month internship as an AI Intern with 52 FPT University students. I worked on three projects: Vietnamese user-review analysis with PhoBERT and XLM-R, a Smart Menu app, and a Vietnamese handwriting dataset. It was my first time doing AI inside a real product team.'), 'hl#aivalley'),
    'cert': (('Chứng chỉ nghiệp vụ sư phạm', '', 'Chứng chỉ bồi dưỡng nghiệp vụ sư phạm dành cho giảng viên đại học. Đây là bước chuẩn bị sớm cho mục tiêu giảng dạy đại học ở cuối con đường.'),
             ('Teaching certificate', '', 'A pedagogy certificate for university lecturers: an early step towards the goal of university teaching at the end of the road.'), None),
    'teky': (('Trợ giảng lập trình, TEKY', '11.2024 – 05.2025', 'Trợ giảng các lớp lập trình tại Học viện Công nghệ TEKY, TP. Hồ Chí Minh. Giải thích một khái niệm cho người mới học buộc tôi phải hiểu nó rõ hơn.'),
             ('Programming TA, TEKY', '11.2024 – 05.2025', 'Teaching assistant for programming classes at TEKY Academy of Technology, Ho Chi Minh City. Explaining a concept to beginners made me understand it better myself.'), None),
    'greenx': (('GREEN-X, VinUniversity', 'từ 04.2026', 'Trung tâm Chuyển đổi xanh thông minh của VinUniversity. Tôi là trợ lý nghiên cứu, làm việc cùng các kỹ sư điện tử, tự động hoá và nhà sinh học biển trên những dự án đưa công nghệ ra biển.'),
               ('GREEN-X, VinUniversity', 'since 04.2026', 'VinUniversity’s Smart Green Transformation Center. I am a research assistant, working with electronics and automation engineers and marine biologists on projects that take technology out to sea.'), None),
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
        wk = {w['slug']: w for w in WORK}; L = 0 if lang == 'vi' else 1
        pj = [dict(slug=s, anchor=a, title=E(tv if lang == 'vi' else te), sub=E(wk[s][lang]['sub']), role=E(wk[s][lang]['role']), when=wk[s]['year'], url='/' + U['workdir'] + s + '.html') for s, a, tv, te in STAGE_PROJECTS.get(i, [])]
        def spot(k):
            t = SPOT_TEXT.get(k); 
            if not t: return None
            ln = t[2]
            if ln: ln = ('/' + U['hl'] + '#' + ln.split('#')[1]) if ln.startswith('hl#') else ln
            return dict(title=E(t[L][0]), when=t[L][1], text=E(t[L][2]), url=ln)
        ms = [dict(kind=k, label=E(lv if lang == 'vi' else le), spot=spot(k)) for k, lv, le in MILESTONES.get(i, [])]
        out.append(dict(when=when, title=d[0], paras=[E(d[1])], lesson=E(d[2]) if len(d) > 2 else '', icon=icon, place=PLACES.get(i, ('', ''))[0 if lang == 'vi' else 1], projects=pj, milestones=ms, greenx=spot('greenx') if icon == 'vinuni' else None, obstacle=OBSTACLE.get(i, 'holes')))
    return E(json.dumps(out, ensure_ascii=False))

def proj_parts(w, lang):
    parts = ''
    for h, paras, items, *_ in w[lang]['body']:
        tag = 'ol' if h in ('Quy trình', 'Pipeline') else 'ul'
        parts += f'<h2>{E(h)}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in paras) + (f'<{tag}>' + ''.join(f'<li>{E(x)}</li>' for x in items) + f'</{tag}>' if items else '')
    lk = ''.join(f'<div><a class="link" href="{u}">{E(n)}</a></div>' for n, u in w['links']) or f'<div>{T[lang]["nolinks"]}</div>'
    return parts, lk

def proj_template(w, lang, p):
    t = T[lang]; d = w[lang]; parts, lk = proj_parts(w, lang)
    return f'''<template id="proj-{w['slug']}"><header class="phead"><div class="mono">{t['p_tag']} · {w['year']}</div><h2>{E(title_of(w, lang))}</h2><p>{E(d['sub'])}</p><div class="pact">{"".join(f'<a href="{u}">{E(nm)}</a>' for nm, u in w['links'])}<a class="alt" href="{rel(p, U['workdir'] + w['slug'] + '.html')}">{t['p_page']}</a></div></header>
<dl class="pmeta"><div><dt>{t['role']}</dt><dd>{E(d['role'])}</dd></div><div><dt>{t['where']}</dt><dd>{E(d['where'])}</dd></div><div><dt>{t['status']}</dt><dd>{E(d['status'])}</dd></div></dl>
<div class="prose">{parts}</div></template>'''

ICON = dict(
 cv='<path d="M14 3v4a1 1 0 0 0 1 1h4"/><path d="M17 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v11a2 2 0 0 1-2 2z"/><path d="M9 17h6M9 13h6"/>',
 scholar='<path d="M22 9 12 5 2 9l10 4 10-4v6"/><path d="M6 10.6V16a6 3 0 0 0 12 0v-5.4"/>',
 github='<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
 linkedin='<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 11v5M8 8v.01M12 16v-5M16 16v-3a2 2 0 0 0-4 0"/>',
 mail='<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 lang='<path d="M4 5h7M9 3v2c0 4.4-2.2 8-5 8"/><path d="M5 9c0 2.1 3 3.9 6.7 4M12 20l4-9 4 9M19.1 18h-6.2"/>')

# ---- trang Giới thiệu (kiểu trang hồ sơ giảng viên) ----
BIO = {
 'vi': ['Tôi là trợ lý nghiên cứu tại GREEN-X (Smart Green Transformation Center), VinUniversity, làm việc dưới sự hướng dẫn của TS. Phùng Mạnh Dương. Tôi tốt nghiệp cử nhân Công nghệ thông tin, chuyên ngành Trí tuệ nhân tạo, tại Trường Đại học FPT năm 2025.',
        'Trước khi đến GREEN-X, tôi thực tập tại FPT AI Creative Valley (Quy Nhơn), làm nghiên cứu viên AI tại Perception Technology Solutions và chuyên viên công nghệ tại VinBigData, chủ yếu với các bài toán thị giác máy tính. Hiện tôi phụ trách xây dựng NTCoral, bộ dữ liệu ảnh rạn san hô Việt Nam, cùng các nhà sinh học biển.',
        'Tôi dự định học tiếp thạc sĩ và tiến sĩ, với mong muốn sau này giảng dạy đại học tại Việt Nam.'],
 'en': ['I am a research assistant at GREEN-X (Smart Green Transformation Center), VinUniversity, working under the supervision of Dr. Phung Manh Duong. I received my bachelor’s degree in Information Technology, with a specialisation in Artificial Intelligence, from FPT University in 2025.',
        'Before GREEN-X, I interned at FPT AI Creative Valley (Quy Nhon), worked as an AI researcher at Perception Technology Solutions and as a technology specialist at VinBigData, mostly on computer vision problems. I currently lead the data work of NTCoral, an image dataset of Vietnamese coral reefs built with marine biologists.',
        'I plan to pursue a master’s degree and a PhD, and later to teach at a university in Vietnam.'],
}
EDU = [('2021 – 2025', ('Cử nhân Công nghệ thông tin, chuyên ngành Trí tuệ nhân tạo', 'Trường Đại học FPT, TP. Hồ Chí Minh', 'Khoá luận: hệ thống đọc khẩu hình tự động dựa trên học sâu. Sinh viên xuất sắc học kỳ Hè 2023.'),
                        ('Bachelor in Information Technology, Artificial Intelligence specialisation', 'FPT University, Ho Chi Minh City', 'Capstone: an automatic lip reading system based on deep learning. Honor Student, Summer 2023.'))]
EXP = [('04.2026 –', ('Trợ lý nghiên cứu', 'GREEN-X, VinUniversity · Hà Nội'), ('Research Assistant', 'GREEN-X, VinUniversity · Hanoi')),
       ('07.2025 – 04.2026', ('Chuyên viên công nghệ (nhánh nghiên cứu AI)', 'VinBigData · Hà Nội'), ('Technology Specialist (AI research track)', 'VinBigData · Hanoi')),
       ('11.2024 – 05.2025', ('Trợ giảng lập trình', 'Học viện Công nghệ TEKY · TP. Hồ Chí Minh'), ('Programming teaching assistant', 'TEKY Academy of Technology · Ho Chi Minh City')),
       ('01.2024 – 07.2025', ('Nghiên cứu viên AI', 'Perception Technology Solutions · làm từ xa'), ('AI Researcher', 'Perception Technology Solutions · remote')),
       ('09 – 12.2023', ('AI Intern', 'FPT AI Creative Valley (AI Valley) · Quy Nhơn'), ('AI Engineer Intern', 'FPT AI Creative Valley (AI Valley) · Quy Nhon'))]
ABOUT_SECS = {'vi': [('bio', 'Tiểu sử'), ('interests', 'Hướng nghiên cứu'), ('education', 'Học vấn'), ('experience', 'Kinh nghiệm'), ('selected', 'Công bố tiêu biểu')],
              'en': [('bio', 'Biography'), ('interests', 'Research interests'), ('education', 'Education'), ('experience', 'Experience'), ('selected', 'Selected publications')]}

def about_page(lang, t, U):
    p = U['about']; vi_ = lang == 'vi'; S = dict(ABOUT_SECS[lang])
    def sec(i, k, inner): return f'<section class="ab-s reveal" id="{k}"><div class="ab-h"><span class="mono">{i:02d}</span><h2>{S[k]}</h2></div><div class="ab-c">{inner}</div></section>'
    bio = ''.join(f'<p>{E(x)}</p>' for x in BIO[lang])
    ints = '<ul class="ab-ri">' + ''.join(f'<li><b>{E(a)}</b><span>{E(d)}</span></li>' for a, d in t['interests']) + '</ul>'
    edu = ''.join(f'<div class="ab-r"><span class="ab-d">{w}</span><div><b>{E(v[0])}</b><span>{E(v[1])}</span><small>{E(v[2])}</small></div></div>' for w, a, b in EDU for v in [a if vi_ else b])
    exp = ''.join(f'<div class="ab-r"><span class="ab-d">{w}</span><div><b>{E(v[0])}</b><span>{E(v[1])}</span></div></div>' for w, a, b in EXP for v in [a if vi_ else b])
    def pub(x):
        y, st, tt, au, vv, ve, u, sl = x
        href = rel(p, U['workdir'] + sl + '.html') if sl else (u or '')
        return f'<div class="ab-r"><span class="ab-d">{y}</span><div><b>{f"<a href={chr(34)}{href}{chr(34)}>{E(tt)}</a>" if href else E(tt)}</b><span class="au">{au}</span><small>{E(vv if vi_ else ve)}</small></div></div>'
    pubs = ''.join(pub(x) for x in PUBS[:3]) + f'<a class="ab-more" href="{rel(p, U["pubs"])}">{"Tất cả công bố" if vi_ else "All publications"} <i>→</i></a>'
    dg = next(m for m in MENTORS if m['slug'] == 'phung-manh-duong')
    lk = (f'<a href="{rel(p, "assets/Aaron_CV.pdf")}">CV ↓</a><a href="{SCHOLAR}" rel="noopener">Google Scholar</a><a href="https://github.com/Zhaninh" rel="noopener">GitHub</a>'
          f'<a href="https://orcid.org/0009-0007-4653-7048" rel="noopener">ORCID</a><a href="https://www.researchgate.net/profile/Ninh-Nguyen-Ngoc-Gia" rel="noopener">ResearchGate</a><a href="{LINKEDIN}" rel="noopener">LinkedIn</a><a href="mailto:{EMAIL_WORK}">Email</a>')
    head_ = (f'<section class="mx ab-top"><div class="wrap"><div class="mx-grid"><div class="mx-l"><figure class="mx-ph"><img src="{rel(p, "assets/people/aaron_tall.webp")}" alt="{E(t["name"].replace("<br>", " "))}"></figure></div>'
             f'<div class="mx-b"><div class="mx-k">{"Giới thiệu" if vi_ else "About"}</div><h1>{t["name"]}</h1><p class="mx-org">Aaron · {E(t["myrole"])}</p>'
             f'<p class="mx-lead">{t["bio"]}</p>'
             f'<ul class="mx-facts"><li>{"Người hướng dẫn" if vi_ else "Supervisor"}: <a href="{rel(p, U["mdir"] + dg["slug"] + ".html")}">{E(dg[lang]["name"])}</a></li></ul>'
             f'<nav class="mx-links">{lk}</nav></div></div></div></section>')
    body = head_ + '<div class="ab"><div class="wrap">' + sec(1, 'bio', bio) + sec(2, 'interests', ints) + sec(3, 'education', edu) + sec(4, 'experience', exp) + sec(5, 'selected', pubs) + '</div></div>'
    write(p, shell(lang, 'about', p, ('Giới thiệu' if vi_ else 'About') + ' · Aaron', body))

def toc_html(lang, path, key, twin):
    """Thanh trên: logo + một viên mục lục (mục đang đọc · ngôn ngữ · ba gạch); bấm mở bảng mục lục, rê chuột vào mục thì hiện mục con."""
    U = URL[lang]; vi_ = lang == 'vi'; r = lambda x: rel(path, x)
    home = r(U['home']) or './'
    sts = sorted(STORIES, key=lambda x: x[0], reverse=True)[:3]
    def nt(tg): return (r(U['hl']) + '#' + tg[1]) if tg[0] == 'hl' else r(U['workdir'] + tg[1] + '.html')
    rows = [
     ('01', 'Giới thiệu' if vi_ else 'About', r(U['about']), [(f'{i+1:02d}', h, r(U['about']) + '#' + k) for i, (k, h) in enumerate(ABOUT_SECS[lang])]),
     ('02', 'Tin mới' if vi_ else 'News', home + '#news', [(d, nv if vi_ else ne, nt(tg)) for d, nv, ne, tg in NEWS if tg]),
     ('03', 'Dự án' if vi_ else 'Projects', home + '#research', [(w['year'].split('–')[0], title_of(w, lang), r(U['workdir'] + w['slug'] + '.html')) for w in RANKED[:4]] + [('→', 'Tất cả dự án' if vi_ else 'All projects', r(U['work']))]),
     ('04', 'Công bố' if vi_ else 'Publications', home + '#pubs', [(x[0], next((title_of(w, lang) for w in WORK if w['slug'] == x[7]), x[2]), r(U['pubs'])) for x in PUBS] + [('→', 'Tất cả công bố' if vi_ else 'All publications', r(U['pubs']))]),
     ('05', 'Người hướng dẫn' if vi_ else 'Mentors', home + '#mentors', [(f'{i+1:02d}', m[lang]['name'], r(U['mdir'] + m['slug'] + '.html')) for i, m in enumerate(MENTORS)]),
     ('06', 'Định hướng' if vi_ else 'Direction', home + '#direction', []),
     ('07', 'Hành trình' if vi_ else 'Journey', r(U['journey']), [((when.split('–')[0] or ('Tiếp' if vi_ else 'Next')), (vi if vi_ else en)[0], r(U['journey']) + f'#stage-{i+1}') for i, (when, vi, en, nx, _) in enumerate(JOURNEY)]),
     ('08', 'Dấu ấn' if vi_ else 'Highlights', r(U['hl']), [(x[1], x[4] if vi_ else x[5], r(U['hl']) + '#' + x[8][0].split('_')[0]) for x in sts]),
    ]
    if path.startswith(U['workdir']): cur = '03'
    elif path.startswith(U['mdir']): cur = '05'
    else: cur = {'journey': '07', 'hl': '08', 'pubs': '04', 'work': '03', 'home': '01', 'about': '01'}.get(key, '')
    names = {n: h for n, h, _, _ in rows}
    start = 'Trang chủ' if vi_ else 'Home'
    li = ''
    for n, h, href, sub in rows:
        fly = (f'<div class="toc-fly{" stack" if max(len(k) for k, _, _ in sub) > 4 else ""}"><ol>' + ''.join(f'<li><a href="{u}"><span class="tn">{E(k)}</span><span class="tt">{E(x)}</span></a></li>' for k, x, u in sub) + '</ol></div>') if sub else ''
        li += f'<li class="toc-i{" has" if sub else ""}{" on" if n == cur else ""}" data-n="{n}"><a href="{href}"><span class="tn">{n}</span><span class="tt">{E(h)}</span></a>{fly}</li>'
    def ic(k, u, lab): return f'<a class="toc-ic" href="{u}" aria-label="{lab}" data-tip="{lab}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg></a>'
    mails = ''.join(f'<a class="ml" href="mailto:{m}"><small>{T[lang][k]}</small>{m}</a>' for k, m in (('mail_work', EMAIL_WORK), ('mail_me', EMAIL)))
    mailbox = (f'<div class="toc-pp"><button type="button" class="toc-ic" aria-label="Email" data-tip="Email" aria-haspopup="true"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON["mail"]}</svg></button>'
               f'<div class="toc-lgpop toc-mlpop"><span class="lgk">2 email</span>{mails}</div></div>')
    icons = ic('cv', r('assets/Aaron_CV.pdf'), 'CV') + ic('scholar', SCHOLAR, 'Google Scholar') + ic('github', 'https://github.com/Zhaninh', 'GitHub') + ic('linkedin', LINKEDIN, 'LinkedIn') + mailbox
    nl_ = 'ngôn ngữ' if vi_ else 'languages'
    opts = ''.join((f'<span class="on" aria-current="true">{nm}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 5 5L20 7"/></svg></span>' if lg == lang else f'<a href="{r(twin)}" hreflang="{lg}" lang="{lg}">{nm}</a>') for lg, nm in (('vi', 'Tiếng Việt'), ('en', 'English')))
    langbox = (f'<div class="toc-lg toc-pp"><button type="button" class="toc-ic" aria-label="{"Ngôn ngữ" if vi_ else "Language"}" aria-haspopup="true"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON["lang"]}</svg></button>'
               f'<div class="toc-lgpop"><span class="lgk">2 {nl_}</span>{opts}</div></div>')
    cn, ct = (cur, names[cur]) if cur else ('', start)
    if cur == '03' and (key == 'work' or path.startswith(U['workdir'])): ct = 'Dự án' if vi_ else 'Projects'
    if cur == '04' and key == 'pubs': ct = 'Công bố' if vi_ else 'Publications'
    return (f'<header class="nav"><a class="brand" href="{home}"><img src="{r("assets/clover.svg")}" alt="">Aaron</a>'
            f'<div class="toc" data-home="{E(start)}" data-names="{E(json.dumps(names, ensure_ascii=False))}">'
            f'<button type="button" class="pill" aria-expanded="false" aria-controls="tocpanel" aria-label="{T[lang]["menu"]}">'
            f'<span class="dot" aria-hidden="true"></span><span class="pn">{cn}</span><span class="pt">{E(ct)}</span><i class="psep"></i>'
            f'<span class="pl">{lang.upper()}</span><i class="psep"></i><span class="hbg" aria-hidden="true"><i></i><i></i><i></i></span></button>'
            f'<div class="toc-lgpop pill-lgpop"><span class="lgk">2 {nl_}</span>{opts}</div>'
            f'<div class="toc-panel" id="tocpanel"><ol class="toc-list">{li}</ol><div class="toc-foot"><div class="toc-icons">{icons}</div></div></div></div></header>')

def shell(lang, key, path, title, body, extra=''):
    t = T[lang]; other = 'en' if lang == 'vi' else 'vi'
    # trang tương ứng ở ngôn ngữ kia
    if path.startswith(URL[lang]['workdir']): twin = URL[other]['workdir'] + os.path.basename(path)
    elif path.startswith(URL[lang]['mdir']): twin = URL[other]['mdir'] + os.path.basename(path)
    else: twin = URL[other][key]
    a = lambda p: rel(path, p)
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><script>(function(){{var h=document.documentElement;h.classList.add('js');setTimeout(function(){{h.classList.add('ready')}},1600);try{{if(sessionStorage.getItem('restore')===location.pathname||(location.hash.length>1&&/(highlights|dau-an)[.]html$/.test(location.pathname))){{h.classList.add('rs');history.scrollRestoration='manual'}}}}catch(e){{}}}})()</script><meta name="description" content="{E(t['slogan_plain'])} Aaron (Nguyen Ngoc Gia Ninh), GREEN-X, VinUniversity.">
<link rel="icon" href="{a('assets/clover.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Be+Vietnam+Pro:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a('assets/style.css')}?v={VER}"></head><body>
{toc_html(lang, path, key, twin)}
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

def guided_html(m, p, lang):
    if not m['guided']: return ''
    vi_ = lang == 'vi'; cards = ''
    for sl, hv, he in m['guided']:
        w = next(x for x in WORK if x['slug'] == sl); href = rel(p, URL[lang]['workdir'] + sl + '.html')
        cov = next((f'assets/projects/{sl}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{sl}.{x}'))), None)
        img = f'<span class="gd-img"><img src="{rel(p, cov)}" alt="" loading="lazy"></span>' if cov else ''
        cards += (f'<a class="gd" href="{href}">{img}<span class="gd-b"><span class="gd-y">{w["year"]}</span><span class="gd-t">{E(title_of(w, lang))}</span>'
                  f'<span class="gd-h">{E(hv if vi_ else he)}</span><span class="gd-go">{"Trang dự án" if vi_ else "Project page"} →</span></span></a>')
    return f'<div class="gd-wrap"><h2>{"Hướng dẫn tôi trong" if vi_ else "Guided my work on"}</h2><div class="gd-list">{cards}</div></div>'

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
        return f'<div class="shead reveal"><div class="sh-t"><span class="sh-n">{k}</span><i aria-hidden="true"></i><h2>{h}</h2></div>{m}</div>'
    def target(tg):
        if not tg: return None
        return rel(p, U['hl']) + '#' + tg[1] if tg[0] == 'hl' else rel(p, U['workdir'] + tg[1] + '.html')
    nl = ''.join((f'<li class="reveal"><time>{d}</time>' + (f'<a href="{target(tg)}">{E(nv if vi_ else ne)} <i>→</i></a>' if tg else f'<span>{E(nv if vi_ else ne)}</span>') + '</li>') for d, nv, ne, tg in NEWS)
    news_html = f'<section class="news" id="news" data-toc="02"><div class="wrap">{sec_head("02", "Tin mới" if vi_ else "News")}<ul class="nlist">{nl}</ul></div></section>'
    def rcard(w, big=False):
        d = w[lang]; href = rel(p, U['workdir'] + w['slug'] + '.html'); c = cov(w['slug'])
        img = f'<span class="rc-img{" fit" if w["slug"] in ("vlr", "vnplant") else ""}" data-cap="{'Xem dự án →' if vi_ else 'View project →'}"><img src="{rel(p, c)}" alt="" loading="lazy"></span>' if c else ''
        return (f'<a class="rc reveal{" big" if big else ""}" href="{href}">{img}<span class="rc-b"><span class="rc-m"><b>{w["year"]}</b><em>{E(d["status"])}</em></span>'
                f'<span class="rc-t">{E(title_of(w, lang))}</span><span class="rc-s">{E(d["sub"])}</span><span class="rc-r">{E(d["role"])}</span><span class="rc-go">{"Trang dự án" if vi_ else "Project page"} →</span></span></a>')
    top = RANKED[:4]; f = top[0]; others = top[1:]
    research_html = (f'<section class="research" id="research" data-toc="03"><div class="wrap">{sec_head("03", "Dự án" if vi_ else "Projects", (rel(p, U["work"]), "Tất cả dự án" if vi_ else "All projects"))}'
                     f'{rcard(f, True)}<div class="rgrid">{"".join(rcard(w) for w in others)}</div></div></section>')
    def hpub(y, st, ti, au, vv, ve, u, sl):
        href = rel(p, U['workdir'] + sl + '.html') if sl else None
        tt = f'<a class="t" href="{u}" rel="noopener">{E(ti)}</a>' if u else f'<span class="t">{E(ti)}</span>'
        acts = (f'<a href="{u}" rel="noopener">{"Bài báo" if vi_ else "Paper"} <i>↗</i></a>' if u else '') + ''.join(f'<a href="{lu}" rel="noopener">{E(lv if vi_ else le)} <i>↗</i></a>' for lv, le, lu in PUB_LINKS.get(sl, [])) + (f'<a href="{href}">{"Dự án" if vi_ else "Project"} <i>→</i></a>' if href else '')
        return f'<li class="reveal"><span class="py mono">{y}</span><div>{tt}<div class="a">{au}</div><div class="v">{E(vv if vi_ else ve)}</div><div class="pl-acts">{acts}</div></div></li>'
    pubs_home = (f'<section class="pubhome" id="pubs" data-toc="04"><div class="wrap">{sec_head("04", "Công bố" if vi_ else "Publications", (rel(p, U["pubs"]), "Tất cả công bố" if vi_ else "All publications"))}'
                 f'<ol class="plist">{"".join(hpub(*x) for x in sorted(PUBS, key=lambda x: next((i for i, w in enumerate(RANKED) if w["slug"] == x[7]), 99))[:3])}</ol></div></section>')
    sts = sorted(STORIES, key=lambda x: x[0], reverse=True)[:3]
    def hcard(st):
        iso, dd, pv, pe, tv, te, sv, se, ims, src, tags = st
        return (f'<a class="hc reveal" href="{rel(p, U["hl"])}#{ims[0].split("_")[0]}"><span class="hc-img" data-cap="{'Xem câu chuyện →' if vi_ else 'Read the story →'}"><img src="{rel(p, "assets/hl/" + ims[0] + ".webp")}" alt="" loading="lazy"></span>'
                f'<span class="hc-m"><time>{dd}</time> · {E(pv if vi_ else pe)}</span><span class="hc-t">{E(tv if vi_ else te)}</span></a>')
    hl_html = (f'<section class="hlhome" id="highlights" data-toc="08"><div class="wrap">{sec_head("08", t["hl"], (rel(p, U["hl"]), "Xem tất cả" if vi_ else "See all"))}'
               f'<div class="hcgrid">{"".join(hcard(x) for x in sts)}</div></div></section>')
    def nb(x):  # giữ các cụm từ không bị ngắt dòng
        for ph in ('Đại học Quốc gia Hà Nội', 'Vietnam National University, Hanoi', 'GREEN-X, VinUniversity'):
            x = x.replace(ph, ph.replace(' ', '&nbsp;'))
        return x
    def mcard(m):
        d = m[lang]; href = rel(p, U['mdir'] + m['slug'] + '.html')
        ini = ''.join(w_[0] for w_ in m['en']['name'].replace('Dr. ', '').split()[:3:2]) if m['en']['name'].count(' ') >= 2 else m['en']['name'][:2]
        av = f'<img src="{rel(p, "assets/people/" + m["photo"] + ".webp")}" alt="{E(d["name"])}" loading="lazy">' if m['photo'] else f'<span class="mc-ini">{ini}</span>'
        return (f'<a class="mc reveal" href="{href}"><span class="mc-av">{av}</span><span class="mc-b"><span class="mc-n">{E(d["name"])}</span>'
                + f'<span class="mc-t">{nb(E(MENTOR_CARD[m["slug"]][0][0 if vi_ else 1]))}</span><span class="mc-r">' + '<br>'.join(f'{E(rv if vi_ else re_)}<br><span class="mc-w">{nb(E(pl))} · <span class="nw">{y0}–{y1 or ("nay" if vi_ else "present")}</span></span>' for rv, re_, pl, y0, y1 in MENTOR_CARD[m['slug']][1]) + '</span>'
                + '</span></a>')
    mentor_html = f'<section class="mentors" id="mentors" data-toc="05"><div class="wrap">{sec_head("05", "Người hướng dẫn" if vi_ else "Mentors")}<div class="mgrid">{"".join(mcard(m) for m in MENTORS)}</div></div></section>'
    three = f'<script src="{rel(p, "assets/three.min.js")}"></script><script src="{rel(p, "assets/journey3d.js")}?v={VER}"></script>'
    body = f'''<section class="hero" id="about" data-toc="01"><div class="wrap"><div class="hero-grid"><div class="hero-l">
<div class="hello">{t['hello']}</div>
<h1 class="name">{t['name']}</h1>
<p class="role">{t['role_pre']} <a class="gxt" href="{GREENX}">GREEN-X, VinUniversity</a></p><div class="typed" data-words="{E(json.dumps(t['words'], ensure_ascii=False))}"></div>
<p class="bio">{t['bio']} <a class="bio-more" href="{rel(p, U['about'])}">{'Giới thiệu đầy đủ' if vi_ else 'Full profile'}&nbsp;→</a></p>
<a class="jbtn" href="{rel(p, U['journey'])}"><span class="ji"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 42c0-10 14-8 16-18S14 12 18 6" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="1 6"/><circle cx="18" cy="6" r="4" fill="currentColor"/><circle cx="8" cy="42" r="3" fill="currentColor"/></svg></span><span class="jt"><b>{t['go_journey']}</b><small>{t['j_sub']}</small></span><span class="ja"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg></span></a></div>
<figure class="pfig reveal"><div class="portrait"><div class="disc"></div><div class="orbit"><i></i></div><img class="me" src="{rel(p, 'assets/aaron_cut.webp')}" alt="{E(t['name'].replace('<br>', ' '))}" width="760" height="1000"></div></figure></div>
<p class="hslogan reveal"><span>{t['slogan']}</span></p>
<div class="kontakt reveal"><div class="kbar"><a class="km" href="mailto:{EMAIL_WORK}"><span class="kic"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/></svg></span><span class="kk">{t['mail_work']}</span><span class="kv">{EMAIL_WORK}</span></a><i class="ksep"></i><a class="km" href="mailto:{EMAIL}"><span class="kic"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/></svg></span><span class="kk">{t['mail_me']}</span><span class="kv">{EMAIL}</span></a><i class="ksep k2"></i><nav class="kl"><a href="{rel(p, 'assets/Aaron_CV.pdf')}">CV<i>↓</i></a><a href="{SCHOLAR}">Scholar<i>↗</i></a><a href="https://github.com/Zhaninh">GitHub<i>↗</i></a><a href="{LINKEDIN}">LinkedIn<i>↗</i></a></nav></div></div></div></section>
{news_html}
{research_html}
{pubs_home}
{mentor_html}
<section class="belief dir" id="direction" data-toc="06"><div class="wrap">{sec_head("06", "Định hướng" if vi_ else "Direction")}<div class="belief-grid"><div class="reveal"><div class="mono">{t['believe']}</div><q>{t['slogan']}</q></div>
<div class="reveal"><div class="mono">{t['h_int']}</div><ol class="ints">{ints}</ol></div></div></div></section>
<section class="teaser-wrap jhome" data-toc="07"><div class="wrap">{sec_head("07", t['t_title'])}<a class="teaser reveal" href="{rel(p, U['journey'])}" data-j3d="teaser" data-stages="{stage_json(lang)}"><canvas></canvas><div class="cap"><div class="mono">{len(JOURNEY)} {t['t_n']}</div><p>{E(t['d_journey'])}</p><span class="btn pri">{t['t_btn']}</span></div></a></div></section>
{hl_html}
'''
    write(p, shell(lang, 'home', p, ('Nguyễn Ngọc Gia Ninh (Aaron)' if lang == 'vi' else 'Nguyen Ngoc Gia Ninh (Aaron)') + ' · ' + t['myrole'], body, three))
    # ---- hành trình ----
    p = U['journey']
    lis = ''.join(f'<li class="reveal{" next" if nx else ""}"><div class="mono">{E(when)}</div><div><h3>{E((vi if lang == "vi" else en)[0])}</h3>{"".join(f"<p>{E(x)}</p>" for x in (vi if lang == "vi" else en)[1:])}{"".join(f"<p><a class=link href={rel(p, U['workdir'] + s + '.html')}>{E(tv if lang == 'vi' else te)}</a></p>" for s, a, tv, te in STAGE_PROJECTS.get(i, []))}</div></li>' for i, (when, vi, en, nx, _) in enumerate(JOURNEY))
    wmap = {w['slug']: w for w in WORK}
    tpls = ''.join(proj_template(wmap[s], lang, p) for i in sorted(STAGE_PROJECTS) for s, a, tv, te in STAGE_PROJECTS[i])
    j3d = f'''<section class="j3d" data-j3d="full" style="--n:9" data-stage="{t['p_stage']}" data-more="{t['more']}" data-less="{t['less']}" data-bump="{t['bump']}" data-unknown="{t['unknown']}" data-future="{E(json.dumps([f[0 if lang == 'vi' else 1] for f in FUTURE], ensure_ascii=False))}" data-pin="{t['p_in']}" data-tag="{t['p_tag']}" {'data-sp-proj="Dự án" data-sp-ms="Cột mốc" data-sp-mine="Phần việc của tôi" data-sp-open="Trang dự án" data-sp-story="Đọc câu chuyện" data-sp-back="Về giai đoạn"' if lang == 'vi' else 'data-sp-proj="Project" data-sp-ms="Milestone" data-sp-mine="My part" data-sp-open="Project page" data-sp-story="Read the story" data-sp-back="Back to stage"'} data-stages="{stage_json(lang)}"><div class="j3d-sticky"><canvas></canvas><div class="j3d-labels"></div>
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
        cv = f'<a class="pc-cover" data-cap="{'Xem dự án →' if lang == 'vi' else 'View project →'}" href="{href}" tabindex="-1" aria-hidden="true"><img src="{rel(p, cov)}" alt="" loading="lazy"></a>' if cov else ''
        return (f'<article class="pc reveal{" star" if w["star"] else ""}">{cv}<div class="pc-top"><span class="pc-y">{w["year"]}</span><span class="pc-s">{E(d["status"])}</span></div>'
                f'<h3><a href="{href}">{E(title_of(w, lang))}</a></h3><p>{E(d["sub"])}</p>'
                f'<div class="pc-meta"><span>{E(d["role"])}</span><span>{E(d["where"])}</span></div>'
                f'<div class="pc-act"><a class="pc-go" href="{href}">{"Chi tiết dự án" if lang == "vi" else "Project page"} <i>→</i></a>{jl}</div></article>')
    vi_w = lang == 'vi'
    def wrow(w):
        d = w[lang]; href = rel(p, U['workdir'] + w['slug'] + '.html'); pb_ = next((x for x in PUBS if x[7] == w['slug']), None)
        acts = f'<a href="{href}">{"Trang dự án" if vi_w else "Project page"} <i>→</i></a>'
        if pb_ and pb_[6]: acts += f'<a href="{pb_[6]}" rel="noopener">{"Bài báo" if vi_w else "Paper"} <i>↗</i></a>'
        acts += ''.join(f'<a href="{lu}" rel="noopener">{E(lv if vi_w else le)} <i>↗</i></a>' for lv, le, lu in PUB_LINKS.get(w['slug'], []))
        c = next((f'assets/projects/{w["slug"]}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{w["slug"]}.{x}'))), None)
        im = f'<a class="wl-img" href="{href}" tabindex="-1" aria-hidden="true"><img src="{rel(p, c)}" alt="" loading="lazy"></a>' if c else '<span class="wl-img"></span>'
        return (f'<li class="reveal">{im}<div><span class="py mono">{w["year"]}</span><a class="t" href="{href}">{E(title_of(w, lang))}</a>'
                f'<div class="s">{E(d["sub"])}</div><div class="v">{E(d["status"])} · {E(d["role"])}</div><div class="pl-acts">{acts}</div></div></li>')
    body_w = (head('Dự án' if vi_w else 'Projects', 'Các dự án nghiên cứu và dữ liệu tôi đã và đang tham gia. Thứ tự được cập nhật tự động hằng tuần theo trạng thái công bố, vai trò, số trích dẫn và lượt tải dữ liệu. Dự án nào có bài báo thì được liệt kê thêm ở trang Công bố.' if vi_w else 'Research and data projects I have worked on. The order updates weekly from publication status, role, citations and dataset downloads. Projects that produced a paper are also listed under Publications.')
              + f'<section><div class="wrap"><ol class="plist wl">{"".join(wrow(w) for w in RANKED)}</ol></div></section>')
    write(p, shell(lang, 'work', p, ('Dự án' if vi_w else 'Projects') + ' · Aaron', body_w))
    onj = {sl for i in STAGE_PROJECTS for sl, *_ in STAGE_PROJECTS[i]}
    for w in WORK:
        d = w[lang]; p = U['workdir'] + w['slug'] + '.html'; vi_ = lang == 'vi'
        pb = next((x for x in PUBS if x[7] == w['slug']), None)
        btns = ''.join(f'<a class="pj-b" href="{u}" rel="noopener">{E(n if vi_ or n != "Chi tiết dự án" else "Project details")} <i>↗</i></a>' for n, u in w['links'])
        from PIL import Image as _I
        def _ar(n):
            with _I.open(os.path.join(ROOT, 'assets/projects/' + n + '.webp')) as _m: return _m.width / _m.height
        def _fig(nm, cap):
            if nm == 'table':
                hdr, rows, best = cap
                th_ = ''.join(f'<th>{E(x)}</th>' for x in hdr)
                tr_ = ''.join(f'<tr{" class=\"best\"" if i == best else ""}>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for i, r in enumerate(rows))
                return f'<div class="x-tabw"><table class="x-tab"><thead><tr>{th_}</tr></thead><tbody>{tr_}</tbody></table></div>'
            nms = nm if isinstance(nm, tuple) else (nm,)
            ims = ''.join(f'<img src="{rel(p, "assets/projects/" + n + ".webp")}" alt="" loading="lazy" style="flex:{_ar(n):.3f} 1 0">' for n in nms)
            return f'<figure class="x-fig{" x-pair" if len(nms) > 1 else ""}"><div class="x-im">{ims}</div><figcaption>{E(cap)}</figcaption></figure>'
        tz = w.get('teaser')
        if tz:
            teaser = f'<figure class="x-fig x-teaser reveal"><div class="x-im"><img src="{rel(p, "assets/projects/" + tz + ".webp")}" alt=""></div>' + (f'<figcaption>{E(d["teaser_cap"])}</figcaption>' if d.get('teaser_cap') else '') + '</figure>'
        else:
            cv_ = next((f'assets/projects/{w["slug"]}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{w["slug"]}.{x}'))), None)
            teaser = f'<figure class="x-fig x-teaser x-cover reveal"><div class="x-im"><img src="{rel(p, cv_)}" alt=""></div></figure>' if cv_ else ''
        stats = ''.join(f'<div><b>{E(n_)}</b><span>{E(l_)}</span></div>' for n_, l_ in d.get('stats', []))
        secs = ''
        for h, paras, items, *fg in d['body']:
            tag = 'ol' if h in ('Quy trình', 'Pipeline') else 'ul'
            inner = ''.join(f'<p>{E(x)}</p>' for x in paras) + (f'<{tag}>' + ''.join(f'<li>{E(x)}</li>' for x in items) + f'</{tag}>' if items else '')
            tabs = ''.join(_fig(*g) for g in fg if g[0] == 'table')
            figs = ''.join(_fig(*g) for g in fg if g[0] != 'table')
            secs += f'<section class="x-s reveal"><h2>{E(h)}</h2><div class="x-body">{inner}{tabs}</div>{figs}</section>'
        if not any(h in ('Phần việc đảm nhận', 'What I did') for h, *_ in d['body']): secs += f'<section class="x-s reveal"><h2>{"Vai trò của tôi" if vi_ else "My role"}</h2><div class="x-body"><p>{E(d["role"])}</p></div></section>'
        cite_h = "Trích dẫn" if vi_ else "Citation"
        if w.get('bib'):
            secs += f'<section class="x-s reveal" id="cite"><h2>{cite_h}</h2><div class="x-body"><pre class="x-bib">{E(w["bib"])}</pre></div></section>'
        elif pb:
            secs += (f'<section class="x-s reveal" id="cite"><h2>{cite_h}</h2><div class="x-body"><p class="pj-cite">{pb[3].rstrip('.')}. {E(pb[2])}. {E(pb[4] if vi_ else pb[5])}.'
                     + (f' <a href="{pb[6]}" rel="noopener">{E(pb[6].replace("https://doi.org/", "doi:"))}</a>' if pb[6] else '') + '</p></div></section>')
        if w.get('bib') or pb: btns += f'<a class="pj-b alt" href="#cite">{cite_h} <i>↓</i></a>'
        body = (f'<section class="x-head"><div class="x-wrap"><div class="pj-meta mono">{E(d["status"])} · <span class="nw">{w["year"]}</span></div><h1>{(d.get("h1") or E(title_of(w, lang))).replace("tiếng Việt", "tiếng&nbsp;Việt").replace("Việt Nam", "Việt&nbsp;Nam")}</h1>'
                + (f'<p class="x-sub">{E(d["dek"])}</p>' if d.get('dek') else '')
                + (f'<p class="pj-au">{pb[3].replace(". ", ".&nbsp;")}</p>' if pb else '') + f'<p class="pj-aff">{E(d["where"])}</p>'
                + (f'<nav class="pj-btns">{btns}</nav>' if btns else '') + f'</div></section>'
                + f'<div class="x-wrap">{teaser}<p class="x-lead reveal">{E(d["sub"])}</p>'
                + (f'<div class="x-stats reveal">{stats}</div>' if stats else '') + f'<div class="x-secs">{secs}</div>'
                + f'<p class="pj-back"><a class="link js-back" href="{rel(p, U["work"])}">{"← Quay lại" if vi_ else "← Back"}</a></p></div>')
        write(p, shell(lang, 'pubs', p, title_of(w, lang) + ' · Aaron', body))
    # ---- công bố ----
    p = U['pubs']
    def cov_of(sl):
        return next((f'assets/projects/{sl}.{x}' for x in ('webp', 'jpg', 'png', 'svg') if os.path.exists(os.path.join(ROOT, f'assets/projects/{sl}.{x}'))), None)
    def pub(y, st, ti, au, vv, ve, u, sl):
        vi_ = lang == 'vi'; href = rel(p, U['workdir'] + sl + '.html') if sl else None
        tt = f'<a class="t" href="{u}" rel="noopener">{E(ti)}</a>' if u else f'<span class="t">{E(ti)}</span>'
        acts = (f'<a href="{u}" rel="noopener">{"Bài báo" if vi_ else "Paper"} <i>↗</i></a>' if u else '')
        acts += ''.join(f'<a href="{lu}" rel="noopener">{E(lv if vi_ else le)} <i>↗</i></a>' for lv, le, lu in PUB_LINKS.get(sl, []))
        acts += (f'<a href="{href}">{"Dự án" if vi_ else "Project"} <i>→</i></a>' if href else '')
        return f'<li class="reveal"><span class="py mono">{y}</span><div>{tt}<div class="a">{au}</div><div class="v">{E(vv if vi_ else ve)}</div><div class="pl-acts">{acts}</div></div></li>'
    lis = ''.join(pub(*x) for x in PUBS)
    write(p, shell(lang, 'pubs', p, t['pubs'] + ' · Aaron', head(t['h_pubs'], t['s_pubs']) + f'<section><div class="wrap"><ol class="plist">{lis}</ol></div></section>'))
    # ---- trang người hướng dẫn ----
    for m in MENTORS:
        d = m[lang]; p = U['mdir'] + m['slug'] + '.html'; vi_ = lang == 'vi'
        lk = ''.join(f'<a href="{u}" rel="noopener">{E(n)}</a>' for n, u in m['links'])
        fx = ''.join(f'<li>{E(x)}</li>' for x in d['facts'])
        body = (f'<section class="mx"><div class="wrap"><div class="mx-grid">'
                f'<div class="mx-l"><figure class="mx-ph">' + (f'<img src="{rel(p, "assets/people/" + m["photo"] + "_tall.webp")}" alt="{E(d["name"])}">' if m['photo'] else f'<span class="mx-ini">{"".join(w_[0] for w_ in m["en"]["name"].split()[::2])}</span>') + f'</figure><a class="mx-back js-back" href="{rel(p, U["home"])}#mentors">← {"Quay lại" if vi_ else "Back"}</a></div>'
                f'<div class="mx-b"><div class="mx-k">{E(d["short"])}</div><h1>{E(d["name"])}</h1>' + f'<p class="mx-org">{E(m.get("org", ("Viện Kỹ thuật và Khoa học Máy tính · VinUniversity", "College of Engineering and Computer Science · VinUniversity"))[0 if vi_ else 1])}</p>'
                + (f'<p class="mx-lead">{E(d["lead"])}</p>' if d['lead'] else '') + (f'<ul class="mx-facts">{fx}</ul>' if fx else '')
                + (f'<div class="mx-mail"><span class="mono">Email</span>' + ''.join(f'<a href="mailto:{x}">{x}</a>' for x in m.get('emails', [])) + '</div>' if m.get('emails') else '')
                + (f'<nav class="mx-links">{lk}</nav>' if lk else '') + '</div></div>' + guided_html(m, p, lang) + '</div></section>')
        write(p, shell(lang, 'home', p, d['name'] + ' · Aaron', body))
    # ---- dấu ấn ----
    p = U['hl']
    def story(st):
        iso, dd, pv, pe, tv, te, sv, se, ims, src, tags = st
        def ar(x):
            try:
                from PIL import Image as _I
                w_, h_ = _I.open(os.path.join(ROOT, 'assets/hl', x + '.webp')).size; return w_ / h_
            except Exception: return 4 / 3
        def btn(x): a_ = ar(x); return f'<button type="button" class="hg-i{' pt' if a_ < 1 else ''}" data-cap="{'Xem ảnh lớn ↗' if lang == 'vi' else 'View full size ↗'}" style="--ar:{a_:.4f}" data-full="{rel(p, "assets/hl/" + x + ".webp")}"><img src="{rel(p, "assets/hl/" + x + ".webp")}" alt="" loading="lazy"></button>'
        im = ''.join(btn(x) for x in ims)
        tg = ''.join(f'<span>{E(x if lang == "vi" else TAG_EN.get(x, x))}</span>' for x in tags)
        sl = ''.join(f'<a href="{u}" rel="noopener">{"Bài gốc" if lang == "vi" else "Original post"} · {E(n)} <i>↗</i></a>' for n, u in src)
        return (f'<article class="hs reveal" id="{ims[0].split("_")[0]}"><div class="hb"><div class="hb-l"><div class="hm"><time datetime="{iso}">{dd}</time><span>{E(pv if lang == "vi" else pe)}</span></div><h3>{E(tv if lang == "vi" else te)}</h3><div class="ht">{tg}</div></div>'
                f'<div class="hb-r"><p>{E(sv if lang == "vi" else se)}</p><div class="hsrc">{sl}</div></div></div><div class="hg n{len(ims)}">{im}</div></article>')
    sts = sorted(STORIES, key=lambda x: x[0], reverse=True)
    body = head(t['h_hl'], t['s_hl']) + f'<section class="hl-wrap"><div class="wrap"><div class="hl-list">{"".join(story(x) for x in sts)}</div></div></section><div class="lb" hidden><button type="button" class="lb-x" aria-label="Close">×</button><img alt=""></div>'
    write(p, shell(lang, 'hl', p, t['hl'] + ' · Aaron', body))
    about_page(lang, t, U)

open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
# README.md được viết tay, build.py không ghi đè
print('ok')
