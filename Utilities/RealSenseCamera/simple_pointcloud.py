import numpy as np
import open3d as o3d
import pyrealsense2 as rs


if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    align = rs.align(rs.stream.color)
    pc = rs.pointcloud()

    vis = o3d.visualization.Visualizer()
    vis.create_window("D435 Point Cloud", 1280, 720)
    render_opt = vis.get_render_option()
    render_opt.point_size = 1.5
    render_opt.background_color = np.asarray([0.0, 0.0, 0.0])

    pcd = o3d.geometry.PointCloud()
    geometry_added = False

    try:
        while True:
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            pc.map_to(color_frame)
            points = pc.calculate(depth_frame)

            verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)
            tex = np.asanyarray(points.get_texture_coordinates()).view(np.float32).reshape(-1, 2)
            color_image = np.asanyarray(color_frame.get_data())[:, :, ::-1] / 255.0

            h, w = color_image.shape[:2]
            u = (tex[:, 0] * w).astype(np.int32)
            v = (tex[:, 1] * h).astype(np.int32)

            valid = (
                (verts[:, 2] > 0)
                & (u >= 0)
                & (u < w)
                & (v >= 0)
                & (v < h)
            )

            xyz = verts[valid]
            rgb = color_image[v[valid], u[valid]]

            pcd.points = o3d.utility.Vector3dVector(xyz)
            pcd.colors = o3d.utility.Vector3dVector(rgb)

            if not geometry_added:
                vis.add_geometry(pcd)
                geometry_added = True
            else:
                vis.update_geometry(pcd)

            if not vis.poll_events():
                break
            vis.update_renderer()

    except KeyboardInterrupt:
        pass
    finally:
        pipeline.stop()
        vis.destroy_window()